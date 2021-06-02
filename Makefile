CC=python3
SOURCE_DIR=source
TARGET_DIR=outputs
EXAMPLE_DIR=example_files

test:
	make build
	make build_example_netlist

	make build_example_pcb
	

build:
	mkdir $(TARGET_DIR)

build_example_json:
	$(CC) $(SOURCE_DIR)/jsongen.py $(EXAMPLE_DIR)/example_layout.json $(TARGET_DIR)
	mv *.kle_json $(TARGET_DIR)

build_example_netlist:
	$(CC) $(SOURCE_DIR)/netlistgen.py $(TARGET_DIR)/outputs.kle_json $(EXAMPLE_DIR)/example_switch_template.config_json $(TARGET_DIR)
	mv netlist* $(TARGET_DIR)

build_example_pcb:
	$(CC) $(SOURCE_DIR)/pcbgen.py $(TARGET_DIR)/outputs.kle_json $(EXAMPLE_DIR)/example_switch_template.config_json $(EXAMPLE_DIR)/example.kicad_pcb $(TARGET_DIR)
	mv mod_$(TARGET_DIR).kicad_pcb $(TARGET_DIR)	

clean:
	rm -rfv $(TARGET_DIR)