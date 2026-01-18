import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import (
    binary_sensor,
    button,
    number,
    sensor,
    switch,
    uart,
)
from esphome.components.uart import UARTComponent
from esphome.const import (
    CONF_ID,
    CONF_INITIAL_VALUE,
    CONF_INTERNAL,
    CONF_NAME,
    CONF_RESTORE_VALUE,
    CONF_STEP,
    CONF_UNIT_OF_MEASUREMENT,
    DEVICE_CLASS_DISTANCE,
    DEVICE_CLASS_OCCUPANCY,
    DEVICE_CLASS_RESTART,
    DEVICE_CLASS_SPEED,
    ENTITY_CATEGORY_CONFIG,
    ENTITY_CATEGORY_DIAGNOSTIC,
    STATE_CLASS_MEASUREMENT,
    UNIT_CENTIMETER,
    UNIT_DEGREES,
    UNIT_METER,
)

MULTI_CONF = True
AUTO_LOAD = ["binary_sensor", "number", "sensor", "button", "switch"]

DEPENDENCIES = ["uart"]

UART_ID = "uart_id"

CONF_USE_FAST_OFF = "fast_off_detection"
CONF_FLIP_X_AXIS = "flip_x_axis"
CONF_OCCUPANCY = "occupancy"
CONF_TARGET_COUNT = "target_count"
CONF_MAX_TILT_ANGLE = "max_detection_tilt_angle"
CONF_MIN_TILT_ANGLE = "min_detection_tilt_angle"
CONF_TILT_ANGLE_MARGIN = "tilt_angle_margin"
CONF_MAX_DISTANCE = "max_detection_distance"
CONF_MAX_DISTANCE_MARGIN = "max_distance_margin"
CONF_TARGETS = "targets"
CONF_TARGET = "target"
CONF_DEBUG = "debug"
CONF_X_SENSOR = "x_position"
CONF_Y_SENSOR = "y_position"
CONF_SPEED_SENSOR = "speed"
CONF_DISTANCE_SENSOR = "distance"
CONF_ANGLE_SENSOR = "angle"
CONF_RESTART_BUTTON = "restart_button"
CONF_TRACKING_MODE_SWITCH = "tracking_mode_switch"
UNIT_METER_PER_SECOND = "m/s"
ICON_ANGLE_ACUTE = "mdi:angle-acute"
ICON_ACCOUNT_GROUP = "mdi:account-group"

ld2450_ns = cg.esphome_ns.namespace("ld2450")
LD2450 = ld2450_ns.class_("LD2450", cg.Component, uart.UARTDevice)
Target = ld2450_ns.class_("Target", cg.Component)
MaxTiltAngleNumber = ld2450_ns.class_("LimitNumber", cg.Component)
MinTiltAngleNumber = ld2450_ns.class_("LimitNumber", cg.Component)
MaxDistanceNumber = ld2450_ns.class_("LimitNumber", cg.Component)
PollingSensor = ld2450_ns.class_("PollingSensor", cg.PollingComponent)
EmptyButton = ld2450_ns.class_("EmptyButton", button.Button, cg.Component)
TrackingModeSwitch = ld2450_ns.class_("TrackingModeSwitch", switch.Switch, cg.Component)
LimitTypeEnum = ld2450_ns.enum("LimitType")


DISTANCE_SENSOR_SCHEMA = (
    sensor.sensor_schema(
        unit_of_measurement=UNIT_METER,
        accuracy_decimals=2,
        state_class=STATE_CLASS_MEASUREMENT,
        device_class=DEVICE_CLASS_DISTANCE,
    )
    .extend(cv.polling_component_schema("1s"))
    .extend(
        {
            cv.GenerateID(): cv.declare_id(PollingSensor),
            cv.Optional(CONF_UNIT_OF_MEASUREMENT, default=UNIT_METER): cv.All(
                cv.one_of(UNIT_METER, UNIT_CENTIMETER),
            ),
        }
    )
)

SPEED_SENSOR_SCHEMA = (
    sensor.sensor_schema(
        unit_of_measurement=UNIT_METER_PER_SECOND,
        accuracy_decimals=0,
        state_class=STATE_CLASS_MEASUREMENT,
        device_class=DEVICE_CLASS_SPEED,
    )
    .extend(cv.polling_component_schema("1s"))
    .extend(
        {
            cv.GenerateID(): cv.declare_id(PollingSensor),
            cv.Optional(
                CONF_UNIT_OF_MEASUREMENT, default=UNIT_METER_PER_SECOND
            ): cv.All(
                cv.one_of(UNIT_METER_PER_SECOND),
            ),
        }
    )
)

DEGREE_SENSOR_SCHEMA = (
    sensor.sensor_schema(
        unit_of_measurement=UNIT_DEGREES,
        accuracy_decimals=0,
        state_class=STATE_CLASS_MEASUREMENT,
        icon=ICON_ANGLE_ACUTE,
    )
    .extend(cv.polling_component_schema("1s"))
    .extend(
        {
            cv.GenerateID(): cv.declare_id(PollingSensor),
            cv.Optional(CONF_UNIT_OF_MEASUREMENT, default=UNIT_DEGREES): cv.All(
                cv.one_of(UNIT_DEGREES),
            ),
        }
    )
)

TARGET_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_TARGET): cv.Schema(
            {
                cv.GenerateID(): cv.declare_id(Target),
                cv.Optional(CONF_NAME): cv.string_strict,
                cv.Optional(CONF_DEBUG, default=False): cv.boolean,
                cv.Optional(CONF_X_SENSOR): DISTANCE_SENSOR_SCHEMA.extend(
                    cv.Schema({cv.Optional(CONF_NAME): cv.string_strict})
                ),
                cv.Optional(CONF_Y_SENSOR): DISTANCE_SENSOR_SCHEMA.extend(
                    cv.Schema({cv.Optional(CONF_NAME): cv.string_strict})
                ),
                cv.Optional(CONF_SPEED_SENSOR): SPEED_SENSOR_SCHEMA.extend(
                    cv.Schema({cv.Optional(CONF_NAME): cv.string_strict})
                ),
                cv.Optional(CONF_ANGLE_SENSOR): DEGREE_SENSOR_SCHEMA.extend(
                    cv.Schema({cv.Optional(CONF_NAME): cv.string_strict})
                ),
                cv.Optional(CONF_DISTANCE_SENSOR): DISTANCE_SENSOR_SCHEMA.extend(
                    cv.Schema({cv.Optional(CONF_NAME): cv.string_strict})
                ),
            }
        ),
    }
)


def validate_target_names(config):
    """
    Validate and set target (and target related sensor) names.
    """
    if target_configs := config.get(CONF_TARGETS):
        for target_index, target_config in enumerate(target_configs):
            target_config_content = target_config[CONF_TARGET]
            if CONF_NAME not in target_config_content:
                target_config_content[CONF_NAME] = f"Target {target_index + 1}"

            for sensor, name_suffix in [
                (CONF_X_SENSOR, "X Position"),
                (CONF_Y_SENSOR, "Y Position"),
                (CONF_SPEED_SENSOR, "Speed"),
                (CONF_ANGLE_SENSOR, "Angle"),
                (CONF_DISTANCE_SENSOR, "Distance"),
            ]:
                if sensor_config := target_config_content.get(sensor):
                    if CONF_NAME in sensor_config and str(
                        sensor_config[CONF_NAME]
                    ) != str(sensor_config[CONF_ID]):
                        sensor_config[CONF_NAME] = (
                            f"{target_config_content[CONF_NAME]} {sensor_config[CONF_NAME]}"
                        )
                    else:
                        sensor_config[CONF_NAME] = (
                            f"{target_config_content[CONF_NAME]} {name_suffix}"
                        )
                        sensor_config[CONF_INTERNAL] = False

    return config


def validate_min_max_angle(config):
    """Assert that the min and max tilt angles do not exceed each other."""

    min_angle = -90
    if subconfig := config.get(CONF_MIN_TILT_ANGLE):
        if isinstance(subconfig, dict):
            min_angle = subconfig[CONF_INITIAL_VALUE]
        elif isinstance(subconfig, float):
            min_angle = subconfig

    max_angle = 90
    if subconfig := config.get(CONF_MAX_TILT_ANGLE):
        if isinstance(subconfig, dict):
            max_angle = subconfig[CONF_INITIAL_VALUE]
        elif isinstance(subconfig, float):
            max_angle = subconfig

    if min_angle >= max_angle:
        raise cv.Invalid(
            f"{CONF_MIN_TILT_ANGLE} must be smaller than {CONF_MAX_TILT_ANGLE} (including initial values)!"
        )

    return config


CONFIG_SCHEMA = cv.All(
    uart.UART_DEVICE_SCHEMA.extend(
        {
            cv.GenerateID(): cv.declare_id(LD2450),
            cv.Required(UART_ID): cv.use_id(UARTComponent),
            cv.Optional(CONF_NAME, default="LD2450"): cv.string_strict,
            cv.Optional(CONF_TARGETS): cv.All(
                cv.ensure_list(TARGET_SCHEMA),
                cv.Length(min=1, max=3),
            ),
            cv.Optional(CONF_FLIP_X_AXIS, default=False): cv.boolean,
            cv.Optional(CONF_USE_FAST_OFF, default=False): cv.boolean,
            cv.Optional(CONF_OCCUPANCY): binary_sensor.binary_sensor_schema(
                device_class=DEVICE_CLASS_OCCUPANCY
            ),
            cv.Optional(CONF_TARGET_COUNT): sensor.sensor_schema(
                accuracy_decimals=0,
            ),
            cv.Optional(CONF_MAX_DISTANCE_MARGIN, default="25cm"): cv.All(
                cv.distance, cv.Range(min=0.0, max=6.0)
            ),
            cv.Optional(CONF_TILT_ANGLE_MARGIN, default="5°"): cv.All(
                cv.angle, cv.Range(min=0.0, max=45.0)
            ),
            cv.Optional(CONF_RESTART_BUTTON): button.button_schema(
                EmptyButton,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
                device_class=DEVICE_CLASS_RESTART,
            ),
            cv.Optional(CONF_TRACKING_MODE_SWITCH): switch.switch_schema(
                TrackingModeSwitch,
                icon=ICON_ACCOUNT_GROUP,
                entity_category=ENTITY_CATEGORY_CONFIG,
            ),
            cv.Optional(CONF_MAX_DISTANCE): cv.Any(
                cv.All(cv.distance, cv.Range(min=0.0, max=6.0)),
                number.number_schema(class_=MaxDistanceNumber)
                .extend(
                    {
                        cv.GenerateID(): cv.declare_id(MaxDistanceNumber),
                        cv.Required(CONF_NAME): cv.string_strict,
                        cv.Optional(CONF_INITIAL_VALUE, default="6.0m"): cv.All(
                            cv.distance, cv.Range(min=0.0, max=6.0)
                        ),
                        cv.Optional(CONF_STEP, default="10cm"): cv.All(
                            cv.distance, cv.Range(min=0.0, max=6.0)
                        ),
                        cv.Optional(CONF_RESTORE_VALUE, default=True): cv.boolean,
                        cv.Optional(
                            CONF_UNIT_OF_MEASUREMENT, default=UNIT_METER
                        ): cv.one_of(UNIT_METER, lower="true"),
                    }
                )
                .extend(cv.COMPONENT_SCHEMA),
            ),
            cv.Optional(CONF_MAX_TILT_ANGLE): cv.Any(
                cv.All(cv.angle, cv.Range(min=-90.0, max=90.0)),
                number.number_schema(class_=MaxTiltAngleNumber)
                .extend(
                    {
                        cv.GenerateID(): cv.declare_id(MaxTiltAngleNumber),
                        cv.Required(CONF_NAME): cv.string_strict,
                        cv.Optional(CONF_INITIAL_VALUE, default="90°"): cv.All(
                            cv.angle,
                            cv.Range(min=-90.0, max=90.0),
                        ),
                        cv.Optional(CONF_STEP, default="1°"): cv.All(
                            cv.angle,
                            cv.Range(min=-90.0, max=90.0),
                        ),
                        cv.Optional(CONF_RESTORE_VALUE, default=True): cv.boolean,
                        cv.Optional(
                            CONF_UNIT_OF_MEASUREMENT, default=UNIT_DEGREES
                        ): cv.one_of(UNIT_DEGREES, lower="true"),
                    }
                )
                .extend(cv.COMPONENT_SCHEMA),
            ),
            cv.Optional(CONF_MIN_TILT_ANGLE): cv.Any(
                cv.All(cv.angle, cv.Range(min=-90.0, max=90.0)),
                number.number_schema(class_=MinTiltAngleNumber)
                .extend(
                    {
                        cv.GenerateID(): cv.declare_id(MinTiltAngleNumber),
                        cv.Required(CONF_NAME): cv.string_strict,
                        cv.Optional(CONF_INITIAL_VALUE, default="-90°"): cv.All(
                            cv.angle,
                            cv.Range(min=-90.0, max=90.0),
                        ),
                        cv.Optional(CONF_STEP, default="1°"): cv.All(
                            cv.angle,
                            cv.Range(min=-90.0, max=90.0),
                        ),
                        cv.Optional(CONF_RESTORE_VALUE, default=True): cv.boolean,
                        cv.Optional(
                            CONF_UNIT_OF_MEASUREMENT, default=UNIT_DEGREES
                        ): cv.one_of(UNIT_DEGREES, lower="true"),
                    }
                )
                .extend(cv.COMPONENT_SCHEMA),
            ),
        }
    ),
    validate_target_names,
    validate_min_max_angle,
)


def to_code(config):
    """Code generation for the LD2450 component."""
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield uart.register_uart_device(var, config)

    cg.add(var.set_name(config[CONF_NAME]))
    cg.add(var.set_flip_x_axis(config[CONF_FLIP_X_AXIS]))
    cg.add(var.set_fast_off_detection(config[CONF_USE_FAST_OFF]))
    cg.add(var.set_max_distance_margin(config[CONF_MAX_DISTANCE_MARGIN]))
    cg.add(var.set_tilt_angle_margin(config[CONF_TILT_ANGLE_MARGIN]))

    # process target list
    if targets_config := config.get(CONF_TARGETS):
        for index, target_config in enumerate(targets_config):
            target = yield target_to_code(target_config[CONF_TARGET], index)
            cg.add(var.register_target(target))

    # Add binary occupancy sensor if present
    if occupancy_config := config.get(CONF_OCCUPANCY):
        occupancy_binary_sensor = yield binary_sensor.new_binary_sensor(
            occupancy_config
        )
        cg.add(var.set_occupancy_binary_sensor(occupancy_binary_sensor))

    # Add target count sensor if present
    if target_count_config := config.get(CONF_TARGET_COUNT):
        target_count_sensor = yield sensor.new_sensor(target_count_config)
        cg.add(var.set_target_count_sensor(target_count_sensor))

    # Different configurations for limit number components
    limit_numbers = {
        CONF_MAX_DISTANCE: {
            "type_enum": LimitTypeEnum.MAX_DISTANCE,
            "min": 0.0,
            "max": 6.0,
        },
        CONF_MAX_TILT_ANGLE: {
            "type_enum": LimitTypeEnum.MAX_TILT_ANGLE,
            "min": -90,
            "max": 90,
        },
        CONF_MIN_TILT_ANGLE: {
            "type_enum": LimitTypeEnum.MIN_TILT_ANGLE,
            "min": -90,
            "max": 90,
        },
    }

    # Add limit values components / fixed numbers
    for _, (key, value) in enumerate(limit_numbers.items()):
        if limit_config := config.get(key):
            # Add number component
            if isinstance(limit_config, dict):
                limit_number = yield number.new_number(
                    limit_config,
                    min_value=value["min"],
                    max_value=value["max"],
                    step=limit_config[CONF_STEP],
                )
                yield cg.register_parented(limit_number, config[CONF_ID])
                yield cg.register_component(limit_number, limit_config)
                cg.add(limit_number.set_initial_state(limit_config[CONF_INITIAL_VALUE]))
                cg.add(limit_number.set_restore(limit_config[CONF_RESTORE_VALUE]))
                cg.add(limit_number.set_type(value["type_enum"]))

                if key == CONF_MAX_DISTANCE:
                    cg.add(var.set_max_distance_number(limit_number))
                elif key == CONF_MAX_TILT_ANGLE:
                    cg.add(var.set_max_angle_number(limit_number))
                elif key == CONF_MIN_TILT_ANGLE:
                    cg.add(var.set_min_angle_number(limit_number))

            elif isinstance(limit_config, float):
                # Set fixed value from simple config
                if key == CONF_MAX_DISTANCE:
                    cg.add(var.set_max_distance(limit_config))
                elif key == CONF_MAX_TILT_ANGLE:
                    cg.add(var.set_max_tilt_angle(limit_config))
                elif key == CONF_MIN_TILT_ANGLE:
                    cg.add(var.set_min_tilt_angle(limit_config))

    # Add sensor restart button if present
    if restart_config := config.get(CONF_RESTART_BUTTON):
        restart_button = yield button.new_button(restart_config)
        cg.add(var.set_restart_button(restart_button))

    # Add tracking mode switch
    if tracking_mode_config := config.get(CONF_TRACKING_MODE_SWITCH):
        mode_switch = cg.new_Pvariable(tracking_mode_config[CONF_ID])
        yield cg.register_parented(mode_switch, config[CONF_ID])
        yield switch.register_switch(mode_switch, tracking_mode_config)
        cg.add(var.set_tracking_mode_switch(mode_switch))


def target_to_code(config, user_index: int):
    """Code generation for targets within the target list."""
    target = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(target, config)

    cg.add(target.set_name(config[CONF_NAME]))
    cg.add(target.set_debugging(config[CONF_DEBUG]))

    for SENSOR in [
        CONF_X_SENSOR,
        CONF_Y_SENSOR,
        CONF_SPEED_SENSOR,
        CONF_ANGLE_SENSOR,
        CONF_DISTANCE_SENSOR,
    ]:
        if sensor_config := config.get(SENSOR):
            sensor_var = cg.new_Pvariable(sensor_config[CONF_ID])
            yield cg.register_component(sensor_var, sensor_config)
            yield sensor.register_sensor(sensor_var, sensor_config)

            if SENSOR == CONF_X_SENSOR:
                cg.add(target.set_x_position_sensor(sensor_var))
            elif SENSOR == CONF_Y_SENSOR:
                cg.add(target.set_y_position_sensor(sensor_var))
            elif SENSOR == CONF_SPEED_SENSOR:
                cg.add(target.set_speed_sensor(sensor_var))
            elif SENSOR == CONF_ANGLE_SENSOR:
                cg.add(target.set_angle_sensor(sensor_var))
            elif SENSOR == CONF_DISTANCE_SENSOR:
                cg.add(target.set_distance_sensor(sensor_var))

    return target
