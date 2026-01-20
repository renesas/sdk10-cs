import sys
from pathlib import Path

from reflect import ReflectTxt

sys.path.append(str(Path(__file__).parent.parent.absolute()))

from qspi.program_qspi_config import ProgramQspiConfig, get_flash_configurations
from api.script_base import ProductId

if __name__ == "__main__":
	product_id, device_flash_name, reflect_path, flash_config_path, = sys.argv[1:]

	reflect = ReflectTxt(Path(reflect_path))

	config = ProgramQspiConfig(flash_config_path)

	config.product_id = ProductId(product_id)
	config.flash_name = device_flash_name

	configurations = get_flash_configurations()
	configuration = configurations[device_flash_name]

	config.flash_size = int(configuration[ProgramQspiConfig.FLASH_SIZE_TAG], 16)
	config.flash_burstcmda_reg_value = int(configuration[ProgramQspiConfig.FLASH_BURSTCMDA_REG_VALUE_TAG], 16)
	config.flash_burstcmdb_reg_value = int(configuration[ProgramQspiConfig.FLASH_BURSTCMDB_REG_VALUE_TAG], 16)
	config.flash_write_config_command = config.parse_config_command(configuration[ProgramQspiConfig.FLASH_WRITE_CONFIG_COMMAND_TAG])

	config.active_image_address = int(reflect.get_symbol_preprocessor("NVMS_FIRMWARE_PART_START"), 16)
	config.update_image_address = config.active_image_address

	config.save()
