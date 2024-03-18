import enum


__all__ = [
    'SensorStateClass',
    'SensorDeviceClass',
    'BinarySensorDeviceClass',
    'CoverDeviceClass',
    'SwitchDeviceClass',
    'LightCommandType',
    'NumberMode',
]


class AvailabilityMode(enum.StrEnum):
    all = 'all'
    any = 'any'
    latest = 'latest'


class SensorStateClass(enum.StrEnum):
    measurement = 'measurement'
    total = 'total'
    total_increasing = 'total_increasing'


class SensorDeviceClass(enum.StrEnum):
    apparent_power = 'apparent_power'              # Apparent power in VA.
    aqi = 'aqi'                                    # Air Quality Index (unitless).
    atmospheric_pressure = 'atmospheric_pressure'  # Atmospheric pressure in cbar, bar, hPa, mmHg, inHg, kPa, mbar, Pa or psi
    battery = 'battery'                            # Percentage of battery that is left in %
    carbon_dioxide = 'carbon_dioxide'              # Carbon Dioxide in CO2(Smoke) in ppm
    carbon_monoxide = 'carbon_monoxide'            # Carbon Monoxide in CO(Gas CNG / LPG) in ppm
    current = 'current'                            # Current in A, mA
    data_rate = 'data_rate'                        # Data rate in bit/s, kbit/s, Mbit/s, Gbit/s, B/s, kB/s, MB/s, GB/s, KiB/s, MiB/s or GiB/s
    data_size = 'data_size'                        # Data size in bit, kbit, Mbit, Gbit, B, kB, MB, GB, TB, PB, EB, ZB, YB, KiB, MiB, GiB, TiB, PiB, EiB, ZiB or YiB
    date = 'date'                                  # Date string (ISO 8601)
    distance = 'distance'                          # Generic distance in km, m, cm, mm, mi, yd, or in
    duration = 'duration'                          # Duration in d, h, min, or s
    energy = 'energy'                              # Energy in Wh, kWh, MWh, MJ, or GJ
    energy_storage = 'energy_storage'              # Stored energy in Wh, kWh, MWh, MJ, or GJ
    enum = 'enum'                                  # Has a limited set of (non-numeric) states
    frequency = 'frequency'                        # Frequency in Hz, kHz, MHz, or GHz
    gas = 'gas'                                    # Gas volume in m³, ft³ or CCF
    humidity = 'humidity'                          # Percentage of humidity in the air in %
    illuminance = 'illuminance'                    # The current light level in lx
    irradiance = 'irradiance'                      # Irradiance in W/m² or BTU/(h⋅ft²)
    moisture = 'moisture'                          # Percentage of water in a substance in %
    monetary = 'monetary'                          # The monetary value (ISO 4217)
    nitrogen_dioxide = 'nitrogen_dioxide'          # Concentration of Nitrogen Dioxide in µg/m³
    nitrogen_monoxide = 'nitrogen_monoxide'        # Concentration of Nitrogen Monoxide in µg/m³
    nitrous_oxide = 'nitrous_oxide'                # Concentration of Nitrous Oxide in µg/m³
    ozone = 'ozone'                                # Concentration of Ozone in µg/m³
    ph = 'ph'                                      # Potential hydrogen (pH) value of a water solution, unitless
    pm1 = 'pm1'                                    # Concentration of particulate matter less than 1 micrometer in µg/m³
    pm25 = 'pm25'                                  # Concentration of particulate matter less than 2.5 micrometers in µg/m³
    pm10 = 'pm10'                                  # Concentration of particulate matter less than 10 micrometers in µg/m³
    power_factor = 'power_factor'                  # Power factor (unitless), unit may be None or %
    power = 'power'                                # Power in W or kW
    precipitation = 'precipitation'                # Accumulated precipitation in cm, in or mm
    pressure = 'pressure'                          # Pressure in Pa, kPa, hPa, bar, cbar, mbar, mmHg, inHg or psi
    reactive_power = 'reactive_power'              # Reactive power in var
    signal_strength = 'signal_strength'            # Signal strength in dB or dBm
    sound_pressure = 'sound_pressure'              # Sound pressure in dB or dBA
    speed = 'speed'                                # Generic speed in ft/s, in/d, in/h, km/h, kn, m/s, mph or mm/d
    sulphur_dioxide = 'sulphur_dioxide'            # Concentration of sulphur dioxide in µg/m³
    temperature = 'temperature'                    # Temperature in °C, °F or K
    timestamp = 'timestamp'                        # Datetime object or timestamp string (ISO 8601)
    volatile_organic_compounds = 'volatile_organic_compounds'  # Concentration of volatile organic compounds in µg/m³
    volatile_organic_compounds_parts = 'volatile_organic_compounds_parts'  # Ratio of volatile organic compounds in ppm or ppb
    voltage = 'voltage'                            # Voltage in V, mV
    volume = 'volume'                              # Generic volume in L, mL, gal, fl. oz., m³, ft³, or CCF
    volume_flow_rate = 'volume_flow_rate'          # Volume flow rate in m³/h, ft³/min, L/min, gal/min
    volume_storage = 'volume_storage'              # Generic stored volume in L, mL, gal, fl. oz., m³, ft³, or CCF
    water = 'water'                                # Water consumption in L, gal, m³, ft³, or CCF
    weight = 'weight'                              # Generic mass in kg, g, mg, µg, oz, lb, or st
    wind_speed = 'wind_speed'                      # Wind speed in ft/s, km/h, kn, m/s, or mph


class BinarySensorDeviceClass(enum.StrEnum):
    battery = 'battery'                            # on means low, off means normal
    battery_charging = 'battery_charging'          # on means charging, off means not charging
    carbon_monoxide = 'carbon_monoxide'            # on means carbon monoxide detected, off no carbon monoxide (clear)
    cold = 'cold'                                  # on means cold, off means normal
    connectivity = 'connectivity'                  # on means connected, off means disconnected
    door = 'door'                                  # on means open, off means closed
    garage_door = 'garage_door'                    # on means open, off means closed
    gas = 'gas'                                    # on means gas detected, off means no gas (clear)
    heat = 'heat'                                  # on means hot, off means normal
    light = 'light'                                # on means light detected, off means no light
    lock = 'lock'                                  # on means open (unlocked), off means closed (locked)
    moisture = 'moisture'                          # on means moisture detected (wet), off means no moisture (dry)
    motion = 'motion'                              # on means motion detected, off means no motion (clear)
    moving = 'moving'                              # on means moving, off means not moving (stopped)
    occupancy = 'occupancy'                        # on means occupied (detected), off means not occupied (clear)
    opening = 'opening'                            # on means open, off means closed
    plug = 'plug'                                  # on means device is plugged in, off means device is unplugged
    power = 'power'                                # on means power detected, off means no power
    presence = 'presence'                          # on means home, off means away
    problem = 'problem'                            # on means problem detected, off means no problem (OK)
    running = 'running'                            # on means running, off means not running
    safety = 'safety'                              # on means unsafe, off means safe
    smoke = 'smoke'                                # on means smoke detected, off means no smoke (clear)
    sound = 'sound'                                # on means sound detected, off means no sound (clear)
    tamper = 'tamper'                              # on means tampering detected, off means no tampering (clear)
    update = 'update'                              # on means update available, off means up-to-date
    vibration = 'vibration'                        # on means vibration detected, off means no vibration (clear)
    window = 'window'                              # on means open, off means closed


class CoverDeviceClass(enum.StrEnum):
    awning = 'awning'
    blind = 'blind'
    curtain = 'curtain'
    damper = 'damper'
    door = 'door'
    garage = 'garage'
    gate = 'gate'
    shade = 'shade'
    shutter = 'shutter'
    window = 'window'


class SwitchDeviceClass(enum.StrEnum):
    outlet = 'outlet'
    switch = 'switch'


class LightCommandType(enum.StrEnum):
    last = 'last'
    first = 'first'


class NumberMode(enum.StrEnum):
    auto = 'auto'
    box = 'box'
    slider = 'slider'
