# pylint: disable=wildcard-import, unused-wildcard-import, protected-access, unused-argument, line-too-long

""" Test the central_configuration """
from unittest.mock import patch  # , call

# from datetime import datetime  # , timedelta
from homeassistant import data_entry_flow
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.core import HomeAssistant

from homeassistant.config_entries import SOURCE_USER
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.versatile_thermostat.thermostat_switch import (
    ThermostatOverSwitch,
)

from custom_components.versatile_thermostat.thermostat_climate import (
    ThermostatOverClimate,
)

from custom_components.versatile_thermostat.vtherm_api import VersatileThermostatAPI

from .commons import *  # pylint: disable=wildcard-import, unused-wildcard-import
from .const import *  # pylint: disable=wildcard-import, unused-wildcard-import


@pytest.mark.parametrize("expected_lingering_tasks", [True])
@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_add_a_central_config(hass: HomeAssistant, skip_hass_states_is_state):
    """Tests the clean_central_config_doubon of base_thermostat"""
    central_config_entry = MockConfigEntry(
        domain=DOMAIN,
        title="TheCentralConfigMockName",
        unique_id="centralConfigUniqueId",
        data={
            CONF_NAME: CENTRAL_CONFIG_NAME,
            CONF_THERMOSTAT_TYPE: CONF_THERMOSTAT_CENTRAL_CONFIG,
            CONF_EXTERNAL_TEMP_SENSOR: "sensor.mock_central_ext_temp_sensor",
            CONF_TEMP_MIN: 15,
            CONF_TEMP_MAX: 30,
            CONF_TPI_COEF_INT: 0.5,
            CONF_TPI_COEF_EXT: 0.02,
            "frost_temp": 10,
            "eco_temp": 17.1,
            "comfort_temp": 18.1,
            "boost_temp": 19.1,
            "eco_ac_temp": 25.1,
            "comfort_ac_temp": 23.1,
            "boost_ac_temp": 21.1,
            "frost_away_temp": 15.1,
            "eco_away_temp": 15.2,
            "comfort_away_temp": 15.3,
            "boost_away_temp": 15.4,
            "eco_ac_away_temp": 30.5,
            "comfort_ac_away_temp": 30.6,
            "boost_ac_away_temp": 30.7,
            CONF_WINDOW_DELAY: 15,
            CONF_WINDOW_AUTO_OPEN_THRESHOLD: 4,
            CONF_WINDOW_AUTO_CLOSE_THRESHOLD: 1,
            CONF_WINDOW_AUTO_MAX_DURATION: 31,
            CONF_MOTION_DELAY: 31,
            CONF_MOTION_OFF_DELAY: 301,
            CONF_MOTION_PRESET: "boost",
            CONF_NO_MOTION_PRESET: "frost",
            CONF_POWER_SENSOR: "sensor.mock_central_power_sensor",
            CONF_MAX_POWER_SENSOR: "sensor.mock_central_max_power_sensor",
            CONF_PRESET_POWER: 14,
            CONF_MINIMAL_ACTIVATION_DELAY: 11,
            CONF_MINIMAL_DEACTIVATION_DELAY: 0,
            CONF_SAFETY_DELAY_MIN: 61,
            CONF_SAFETY_MIN_ON_PERCENT: 0.5,
            CONF_SAFETY_DEFAULT_ON_PERCENT: 0.2,
            CONF_USE_CENTRAL_BOILER_FEATURE: False,
        },
    )

    entity = await create_thermostat(
        hass, central_config_entry, "climate.thecentralconfigmockname"
    )
    # central_config_entry.add_to_hass(hass)
    # await hass.config_entries.async_setup(central_config_entry.entry_id)
    # assert central_config_entry.state is ConfigEntryState.LOADED
    #
    # entity: ThermostatOverClimate = search_entity(
    #    hass, "climate.thecentralconfigmockname", "climate"
    # )

    assert entity is None

    assert count_entities(hass, "climate.thecentralconfigmockname", "climate") == 0

    # Test that VTherm API find the CentralConfig
    api = VersatileThermostatAPI.get_vtherm_api(hass)
    central_configuration = api.find_central_configuration()
    assert central_configuration is not None

    # Test that VTherm API doesn't have any central boiler entities
    assert api.nb_active_device_for_boiler_entity is None
    assert api.nb_active_device_for_boiler is None

    assert api.nb_active_device_for_boiler_threshold_entity is None
    assert api.nb_active_device_for_boiler_threshold is None


# @pytest.mark.parametrize("expected_lingering_tasks", [True])
@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_minimal_over_switch_wo_central_config(
    hass: HomeAssistant, skip_hass_states_is_state, init_vtherm_api
):
    """Tests that a VTherm without any central_configuration is working with its own attributes"""
    # Add a Switch VTherm
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="TheOverSwitchMockName",
        unique_id="uniqueId",
        data={
            CONF_NAME: "TheOverSwitchMockName",
            CONF_THERMOSTAT_TYPE: CONF_THERMOSTAT_SWITCH,
            CONF_TEMP_SENSOR: "sensor.mock_temp_sensor",
            CONF_EXTERNAL_TEMP_SENSOR: "sensor.mock_ext_temp_sensor",
            CONF_CYCLE_MIN: 5,
            CONF_TEMP_MIN: 8,
            CONF_TEMP_MAX: 18,
            CONF_STEP_TEMPERATURE: 0.3,
            "frost_temp": 10,
            "eco_temp": 17,
            "comfort_temp": 18,
            "boost_temp": 21,
            CONF_USE_WINDOW_FEATURE: False,
            CONF_USE_MOTION_FEATURE: False,
            CONF_USE_POWER_FEATURE: False,
            CONF_USE_PRESENCE_FEATURE: False,
            CONF_HEATER: "switch.mock_switch",
            CONF_PROP_FUNCTION: PROPORTIONAL_FUNCTION_TPI,
            CONF_TPI_COEF_INT: 0.3,
            CONF_TPI_COEF_EXT: 0.01,
            CONF_MINIMAL_ACTIVATION_DELAY: 30,
            CONF_MINIMAL_DEACTIVATION_DELAY: 0,
            CONF_SAFETY_DELAY_MIN: 5,
            CONF_SAFETY_MIN_ON_PERCENT: 0.3,
            CONF_SAFETY_DEFAULT_ON_PERCENT: 0.1,
            # CONF_WINDOW_AUTO_OPEN_THRESHOLD: 0.1,
            # CONF_WINDOW_AUTO_CLOSE_THRESHOLD: 0.1,
            # CONF_WINDOW_AUTO_MAX_DURATION: 0,  # Should be 0 for test
            CONF_INVERSE_SWITCH: True,
            # CONF_USE_MAIN_CENTRAL_CONFIG: False,
            # CONF_USE_TPI_CENTRAL_CONFIG: False,
            # CONF_USE_WINDOW_CENTRAL_CONFIG: False,
            # CONF_USE_MOTION_CENTRAL_CONFIG: False,
            # CONF_USE_POWER_CENTRAL_CONFIG: False,
            # CONF_USE_PRESENCE_CENTRAL_CONFIG: False,
            # CONF_USE_PRESETS_CENTRAL_CONFIG: False,
            # CONF_USE_ADVANCED_CENTRAL_CONFIG: False,
        },
    )

    with patch("homeassistant.core.ServiceRegistry.async_call"):
        entity: ThermostatOverSwitch = await create_thermostat(
            hass, entry, "climate.theoverswitchmockname"
        )
        assert entity
        assert entity.name == "TheOverSwitchMockName"
        assert entity.is_over_switch
        assert entity._temp_sensor_entity_id == "sensor.mock_temp_sensor"
        assert entity._ext_temp_sensor_entity_id == "sensor.mock_ext_temp_sensor"
        assert entity._cycle_min == 5
        assert entity.min_temp == 8
        assert entity.max_temp == 18
        assert entity.target_temperature_step == 0.3
        assert entity.preset_modes == ["none", "frost", "eco", "comfort", "boost"]
        assert entity.window_manager.is_window_auto_configured is False
        assert entity.nb_underlying_entities == 1
        assert entity.underlying_entity_id(0) == "switch.mock_switch"
        assert entity.proportional_algorithm is not None
        assert entity.proportional_algorithm._tpi_coef_int == 0.3
        assert entity.proportional_algorithm._tpi_coef_ext == 0.01
        assert entity.proportional_algorithm._minimal_activation_delay == 30
        assert entity.safety_manager.safety_delay_min == 5
        assert entity.safety_manager.safety_min_on_percent == 0.3
        assert entity.safety_manager.safety_default_on_percent == 0.1
        assert entity.is_inversed

    entity.remove_thermostat()


@pytest.mark.parametrize("expected_lingering_tasks", [True])
@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_full_over_switch_wo_central_config(
    hass: HomeAssistant, skip_hass_states_is_state, init_vtherm_api
):
    """Tests that a VTherm without any central_configuration is working with its own attributes"""

    temps = {
        "frost": 10,
        "eco": 17,
        "comfort": 18,
        "boost": 21,
        "frost_away": 13,
        "eco_away": 13,
        "comfort_away": 13,
        "boost_away": 13,
    }

    # Add a Switch VTherm
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="TheOverSwitchMockName",
        unique_id="uniqueId",
        data={
            CONF_NAME: "TheOverSwitchMockName",
            CONF_THERMOSTAT_TYPE: CONF_THERMOSTAT_SWITCH,
            CONF_TEMP_SENSOR: "sensor.mock_temp_sensor",
            CONF_EXTERNAL_TEMP_SENSOR: "sensor.mock_ext_temp_sensor",
            CONF_CYCLE_MIN: 5,
            CONF_TEMP_MIN: 8,
            CONF_TEMP_MAX: 18,
            CONF_STEP_TEMPERATURE: 0.3,
            CONF_USE_WINDOW_FEATURE: True,
            CONF_USE_MOTION_FEATURE: True,
            CONF_USE_POWER_FEATURE: True,
            CONF_USE_PRESENCE_FEATURE: True,
            CONF_UNDERLYING_LIST: ["switch.mock_switch"],
            CONF_PROP_FUNCTION: PROPORTIONAL_FUNCTION_TPI,
            CONF_INVERSE_SWITCH: False,
            CONF_TPI_COEF_INT: 0.3,
            CONF_TPI_COEF_EXT: 0.01,
            CONF_MINIMAL_ACTIVATION_DELAY: 30,
            CONF_MINIMAL_DEACTIVATION_DELAY: 0,
            CONF_SAFETY_DELAY_MIN: 5,
            CONF_SAFETY_MIN_ON_PERCENT: 0.3,
            CONF_SAFETY_DEFAULT_ON_PERCENT: 0.1,
            CONF_WINDOW_SENSOR: "binary_sensor.mock_window_sensor",
            CONF_WINDOW_DELAY: 30,
            CONF_WINDOW_AUTO_OPEN_THRESHOLD: 3,
            CONF_WINDOW_AUTO_CLOSE_THRESHOLD: 0.1,
            CONF_WINDOW_AUTO_MAX_DURATION: 5,
            CONF_MOTION_DELAY: 10,
            CONF_MOTION_OFF_DELAY: 29,
            CONF_MOTION_PRESET: "comfort",
            CONF_NO_MOTION_PRESET: "eco",
            CONF_MOTION_SENSOR: "binary_sensor.mock_motion_sensor",
            CONF_PRESENCE_SENSOR: "binary_sensor.mock_presence_sensor",
            CONF_USE_MAIN_CENTRAL_CONFIG: False,
            CONF_USE_TPI_CENTRAL_CONFIG: False,
            CONF_USE_WINDOW_CENTRAL_CONFIG: False,
            CONF_USE_MOTION_CENTRAL_CONFIG: False,
            CONF_USE_POWER_CENTRAL_CONFIG: False,
            CONF_USE_PRESENCE_CENTRAL_CONFIG: False,
            CONF_USE_PRESETS_CENTRAL_CONFIG: False,
            CONF_USE_ADVANCED_CENTRAL_CONFIG: False,
        },
    )

    with patch("homeassistant.core.ServiceRegistry.async_call"):
        entity: ThermostatOverSwitch = await create_thermostat(
            hass, entry, "climate.theoverswitchmockname", temps
        )
        assert entity
        assert entity.name == "TheOverSwitchMockName"
        assert entity.is_over_switch
        assert entity._temp_sensor_entity_id == "sensor.mock_temp_sensor"
        assert entity._ext_temp_sensor_entity_id == "sensor.mock_ext_temp_sensor"
        assert entity._cycle_min == 5
        assert entity.min_temp == 8
        assert entity.max_temp == 18
        assert entity.target_temperature_step == 0.3
        assert entity.preset_modes == [
            "none",
            "frost",
            "eco",
            "comfort",
            "boost",
            "activity",
        ]
        assert entity.nb_underlying_entities == 1
        assert entity.underlying_entity_id(0) == "switch.mock_switch"
        assert entity.proportional_algorithm is not None
        assert entity.proportional_algorithm._tpi_coef_int == 0.3
        assert entity.proportional_algorithm._tpi_coef_ext == 0.01
        assert entity.proportional_algorithm._minimal_activation_delay == 30
        assert entity.safety_manager.safety_delay_min == 5
        assert entity.safety_manager.safety_min_on_percent == 0.3
        assert entity.safety_manager.safety_default_on_percent == 0.1
        assert entity.is_inversed is False

        assert (
            entity.window_manager.is_window_auto_configured is False
        )  # we have an entity_id
        assert (
            entity.window_manager._window_sensor_entity_id
            == "binary_sensor.mock_window_sensor"
        )
        assert entity.window_manager.window_delay_sec == 30
        assert entity.window_manager.window_auto_close_threshold == 0.1
        assert entity.window_manager.window_auto_open_threshold == 3
        assert entity.window_manager.window_auto_max_duration == 5

        assert (
            entity.motion_manager.motion_sensor_entity_id
            == "binary_sensor.mock_motion_sensor"
        )
        assert entity.motion_manager.motion_delay_sec == 10
        assert entity.motion_manager.motion_off_delay_sec == 29
        assert entity.motion_manager.motion_preset == "comfort"
        assert entity.motion_manager.no_motion_preset == "eco"

        assert (
            VersatileThermostatAPI.get_vtherm_api().central_power_manager.power_sensor_entity_id
            is None
        )
        assert (
            VersatileThermostatAPI.get_vtherm_api().central_power_manager.max_power_sensor_entity_id
            is None
        )

        assert (
            entity._presence_manager.presence_sensor_entity_id
            == "binary_sensor.mock_presence_sensor"
        )

    entity.remove_thermostat()


@pytest.mark.parametrize("expected_lingering_tasks", [True])
@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_full_over_switch_with_central_config(
    hass: HomeAssistant, skip_hass_states_is_state, init_central_power_manager
):
    """Tests that a VTherm with central_configuration is working with the central_config attributes"""
    # Add a Switch VTherm
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="TheOverSwitchMockName",
        unique_id="uniqueId",
        data={
            CONF_NAME: "TheOverSwitchMockName",
            CONF_THERMOSTAT_TYPE: CONF_THERMOSTAT_SWITCH,
            CONF_TEMP_SENSOR: "sensor.mock_temp_sensor",
            CONF_EXTERNAL_TEMP_SENSOR: "sensor.mock_ext_temp_sensor",
            CONF_CYCLE_MIN: 5,
            CONF_TEMP_MIN: 8,
            CONF_TEMP_MAX: 18,
            CONF_STEP_TEMPERATURE: 0.3,
            CONF_USE_WINDOW_FEATURE: True,
            CONF_USE_MOTION_FEATURE: True,
            CONF_USE_POWER_FEATURE: True,
            CONF_USE_PRESENCE_FEATURE: True,
            CONF_UNDERLYING_LIST: ["switch.mock_switch"],
            CONF_PROP_FUNCTION: PROPORTIONAL_FUNCTION_TPI,
            CONF_INVERSE_SWITCH: False,
            CONF_TPI_COEF_INT: 0.3,
            CONF_TPI_COEF_EXT: 0.01,
            CONF_MINIMAL_ACTIVATION_DELAY: 30,
            CONF_MINIMAL_DEACTIVATION_DELAY: 0,
            CONF_SAFETY_DELAY_MIN: 5,
            CONF_SAFETY_MIN_ON_PERCENT: 0.3,
            CONF_SAFETY_DEFAULT_ON_PERCENT: 0.1,
            CONF_WINDOW_SENSOR: "binary_sensor.mock_window_sensor",
            CONF_WINDOW_DELAY: 30,
            CONF_WINDOW_AUTO_OPEN_THRESHOLD: 3,
            CONF_WINDOW_AUTO_CLOSE_THRESHOLD: 0.1,
            CONF_WINDOW_AUTO_MAX_DURATION: 5,
            CONF_MOTION_DELAY: 10,
            CONF_MOTION_OFF_DELAY: 29,
            CONF_MOTION_PRESET: "comfort",
            CONF_NO_MOTION_PRESET: "eco",
            CONF_MOTION_SENSOR: "binary_sensor.mock_motion_sensor",
            CONF_PRESENCE_SENSOR: "binary_sensor.mock_presence_sensor",
            CONF_USE_MAIN_CENTRAL_CONFIG: True,
            CONF_USE_TPI_CENTRAL_CONFIG: True,
            CONF_USE_WINDOW_CENTRAL_CONFIG: True,
            CONF_USE_MOTION_CENTRAL_CONFIG: True,
            CONF_USE_POWER_CENTRAL_CONFIG: True,
            CONF_USE_PRESENCE_CENTRAL_CONFIG: True,
            CONF_USE_PRESETS_CENTRAL_CONFIG: True,
            CONF_USE_ADVANCED_CENTRAL_CONFIG: True,
        },
    )

    with patch("homeassistant.core.ServiceRegistry.async_call"):
        entity: ThermostatOverSwitch = await create_thermostat(
            hass, entry, "climate.theoverswitchmockname"
        )
        assert entity
        assert entity.name == "TheOverSwitchMockName"
        assert entity.is_over_switch
        assert entity._temp_sensor_entity_id == "sensor.mock_temp_sensor"
        assert entity._ext_temp_sensor_entity_id == "sensor.mock_ext_temp_sensor"
        assert entity._cycle_min == 5
        assert entity.min_temp == 15
        assert entity.max_temp == 30
        assert entity.target_temperature_step == 0.1
        assert entity.preset_modes == [
            "none",
            "frost",
            "eco",
            "boost",
            "activity",
        ]
        assert entity.nb_underlying_entities == 1
        assert entity.underlying_entity_id(0) == "switch.mock_switch"
        assert entity.proportional_algorithm is not None
        assert entity.proportional_algorithm._tpi_coef_int == 0.5
        assert entity.proportional_algorithm._tpi_coef_ext == 0.02
        assert entity.proportional_algorithm._minimal_activation_delay == 11
        assert entity.safety_manager.safety_delay_min == 61
        assert entity.safety_manager.safety_min_on_percent == 0.5
        assert entity.safety_manager.safety_default_on_percent == 0.2
        assert entity.is_inversed is False

        # We have an entity so window auto is not enabled
        assert entity.window_manager.is_window_auto_configured is False
        assert (
            entity.window_manager._window_sensor_entity_id
            == "binary_sensor.mock_window_sensor"
        )
        assert entity.window_manager.window_delay_sec == 15
        assert entity.window_manager.window_auto_close_threshold == 1
        assert entity.window_manager.window_auto_open_threshold == 4
        assert entity.window_manager.window_auto_max_duration == 31

        assert (
            entity.motion_manager.motion_sensor_entity_id
            == "binary_sensor.mock_motion_sensor"
        )
        assert entity.motion_manager.motion_delay_sec == 31
        assert entity.motion_manager.motion_off_delay_sec == 301
        assert entity.motion_manager.motion_preset == "boost"
        assert entity.motion_manager.no_motion_preset == "frost"

        assert (
            VersatileThermostatAPI.get_vtherm_api().central_power_manager.power_sensor_entity_id
            == "sensor.the_power_sensor"
        )
        assert (
            VersatileThermostatAPI.get_vtherm_api().central_power_manager.max_power_sensor_entity_id
            == "sensor.the_max_power_sensor"
        )

        assert (
            entity._presence_manager.presence_sensor_entity_id
            == "binary_sensor.mock_presence_sensor"
        )

    entity.remove_thermostat()


# @pytest.mark.parametrize("expected_lingering_tasks", [True])
# @pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_over_switch_with_central_config_but_no_central_config(
    hass: HomeAssistant, skip_hass_states_get, init_vtherm_api
):
    """Tests that a VTherm with a central_configuration flag but no central config. Should lead to an error"""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == SOURCE_USER

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_THERMOSTAT_TYPE: CONF_THERMOSTAT_SWITCH,
        },
    )

    assert result["type"] == FlowResultType.MENU
    assert result["step_id"] == "menu"
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input={"next_step_id": "main"}
    )

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "main"
    assert result["errors"] == {}

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_NAME: "TheOverSwitchMockName",
            CONF_TEMP_SENSOR: "sensor.mock_temp_sensor",
            CONF_CYCLE_MIN: 5,
            CONF_DEVICE_POWER: 1,
            CONF_USE_MAIN_CENTRAL_CONFIG: True,
        },
    )

    assert result["type"] == FlowResultType.FORM
    # in case of error we stays in main
    assert result["step_id"] == "main"
    assert result["errors"] == {"use_main_central_config": "no_central_config"}


async def test_migration_of_central_config(
    hass: HomeAssistant,
    skip_hass_states_is_state,
):
    """Tests the clean_central_config_doubon of base_thermostat"""
    central_config_entry = MockConfigEntry(
        version=CONFIG_VERSION,
        # An old minor version
        minor_version=0,
        domain=DOMAIN,
        title="TheCentralConfigMockName",
        unique_id="centralConfigUniqueId",
        data={
            CONF_NAME: CENTRAL_CONFIG_NAME,
            CONF_THERMOSTAT_TYPE: CONF_THERMOSTAT_CENTRAL_CONFIG,
            CONF_EXTERNAL_TEMP_SENSOR: "sensor.mock_ext_temp_sensor",
            CONF_TEMP_MIN: 15,
            CONF_TEMP_MAX: 30,
            CONF_STEP_TEMPERATURE: 0.1,
            CONF_TPI_COEF_INT: 0.5,
            CONF_TPI_COEF_EXT: 0.02,
            CONF_MINIMAL_ACTIVATION_DELAY: 11,
            CONF_MINIMAL_DEACTIVATION_DELAY: 0,
            CONF_SAFETY_DELAY_MIN: 61,
            CONF_SAFETY_MIN_ON_PERCENT: 0.5,
            CONF_SAFETY_DEFAULT_ON_PERCENT: 0.2,
            # The old central_boiler parameter
            "add_central_boiler_control": True,
            CONF_CENTRAL_BOILER_ACTIVATION_SRV: "switch.pompe_chaudiere/switch.turn_on",
            CONF_CENTRAL_BOILER_DEACTIVATION_SRV: "switch.pompe_chaudiere/switch.turn_off",
        },
    )

    central_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(central_config_entry.entry_id)
    assert central_config_entry.state is ConfigEntryState.LOADED

    entity: ThermostatOverClimate = search_entity(
        hass, "climate.thecentralconfigmockname", "climate"
    )

    assert entity is None

    assert count_entities(hass, "climate.thecentralconfigmockname", "climate") == 0

    # Test that VTherm API find the CentralConfig
    api = VersatileThermostatAPI.get_vtherm_api(hass)
    central_configuration = api.find_central_configuration()
    assert central_configuration is not None

    assert central_config_entry.data.get(CONF_USE_CENTRAL_BOILER_FEATURE) is True

    # Test that VTherm API have any central boiler entities
    # It should have been migrated and initialized
    assert api.nb_active_device_for_boiler_entity is not None
    assert api.nb_active_device_for_boiler == 0

    assert api.nb_active_device_for_boiler_threshold_entity is not None
    assert api.nb_active_device_for_boiler_threshold == 1  # the default value is 1
