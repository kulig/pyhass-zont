class Entity:
    """
    Базовый класс для определения MQTT-сущностей, которые понимаются Home Assistant.
    https://www.home-assistant.io/integrations/mqtt/
    """

    def __init__(
        self,
        id_: str,
        model_cls: type,
    ) -> None:
        """
        :param id_: Строка, содержащая уникальный идентификатор сущности в рамках Node.
        :param model_cls: Класс (фабрика) модели сущности. См. pyhass_mqtt.models или
                          https://www.home-assistant.io/integrations/mqtt/
        """
        self.model = model_cls()
        self.id = id_
        self.discovery_topic: str | None = None

    def set_node(self, node: t.Optional["Node"]) -> None:
        """
        В этом методе устанавливается node, владеющая данной сущностью.
        В наследниках этого класса следует переопределять этот метод для вычисления имен топиков и прочего,
        зависящего от ноды или ее имени. При переопределении обязательно сначала вызвать родительскую реализацию метода.

        :param node: Экземпляр класса Node или None
        """
        self.node = node
        if node is not None:
            self.model.object_id = self.model.unique_id = f"{node.id}_{self.id}"
            self.model.state_topic = f"{node.id}/{self.id}/state"
            self.model.device = node.device
            self.discovery_topic = f"{node.discovery_prefix}/{self.model.discovery_class_}/{node.id}/{self.id}/config"
        else:
            self.model.unique_id = None
            self.model.object_id = None
            self.model.state_topic = None
            self.model.device = None
            self.discovery_topic = None

    def subscribe(self) -> None:
        """
        Этот метод вызывается нодой, чтобы данная сущность подписалась на все интересующие ее топики.
        В наследниках этого класса при переопределении сначала желательно вызвать родительскую реализацию.

        Чтобы подписаться, используем:
            self.node.client.subscribe(topic)
            self.node.client.message_callback_add(topic, on_msg)
        Обработчик должен быть таким:
            def on_msg(client: mqtt.Client, userdata: t.Any, message: mqtt.MQTTMessage) -> None
        """
        if self.node is None:
            raise RuntimeError("Cannot subscribe entity without node")

    def unsubscribe(self) -> None:
        """
        Этот метод вызывается нодой, чтобы сущность отписалась от всех топиков, на которые была подписана.
        В наследниках этого класса при переопределении сначала желательно вызвать родительскую реализацию.

        Чтобы отписаться, используем:
            self.node.client.message_callback_remove(topic)
            self.node.client.unsubscribe(topic)
        """
        if self.node is None:
            raise RuntimeError("Cannot unsubscribe entity without node")

    def get_state(self) -> str:
        """
        Этот метод обязателен к переопределению в наследниках класса.

        :return: Текущее состояние (state) сущности.
        """
        raise NotImplementedError("get_state")

    def publish_state(self) -> None:
        """
        При вызове этого метода, сущность опубликует в своем state_topic свое состояние (см. get_state())
        """
        if self.node is None:
            raise RuntimeError("Cannot publish state of entity without node")
        self.node.client.publish(
            self.model.state_topic,
            self.get_state().encode(self.model.encoding),
            self.model.qos,
            self.model.retain,
        )

    def publish_discovery(self) -> None:
        """
        Этот метод публикует MQTT discovery JSON для Home Assistant в соответствующем топике.
        Метод вызывается нодой.
        Для генерации discovery JSON используется экземпляр модели сущности (см. конструктор)
        """
        if self.node is None:
            raise RuntimeError("Cannot publish discovery of entity without node")
        self.node.client.publish(
            self.discovery_topic, self.model.discovery_json(), 1, False
        )

    def unpublish_discovery(self) -> None:
        """
        Этот метод публикует пустую строку для Home Assistant в топике для MQTT discovery.
        Метод вызывается нодой.
        """
        if self.node is None:
            raise RuntimeError("Cannot un-publish discovery of entity without node")
        self.node.client.publish(self.discovery_topic, "", 1, False)
