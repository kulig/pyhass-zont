help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


test:  ## Запуск тестов (mypy, ruff)
	mypy $(CURDIR)
	ruff check $(CURDIR)


clean:  ## Очистка кэша
	rm -r $(CURDIR)/.mypy_cache
	rm -r $(CURDIR)/.ruff_cache
