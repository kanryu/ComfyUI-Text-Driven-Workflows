import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "TextDrivenWorkflows.TextLineSelector", // 拡張機能の登録名を変更
    async nodeCreated(node) {
        if (node.comfyClass === "TextDrivenTextLineSelector") { // 新しいノードIDをターゲットにする
            const listWidget = node.widgets.find(w => w.name === "text_list");
            const comboWidget = node.widgets.find(w => w.name === "selected_line");

            if (listWidget && comboWidget) {
                const updateComboOptions = (textValue) => {
                    if (!textValue) return;
                    
                    // Split raw text into clean rows, explicitly skipping empty lines
                    const lines = textValue.split("\n")
                        .map(line => line.trim())
                        .filter(line => line.length > 0);
                    
                    const displayLabels = [];
                    const valueMap = {};

                    lines.forEach(line => {
                        if (line.includes("|-|")) {
                            const parts = line.split("|-|");
                            const label = parts[0].trim();
                            const value = parts[1].trim();
                            
                            // Ensure the label isn't blank before registering
                            if (label.length > 0) {
                                displayLabels.push(label);
                                valueMap[label] = value; // Map UI label to Backend value
                            }
                        } else {
                            // Fallback: No separator found, use the full line for both label and value
                            displayLabels.push(line);
                            valueMap[line] = line;
                        }
                    });
                    
                    // Attach the dynamic lookup dictionary to the widget instance
                    comboWidget.customValueMap = valueMap;
                    
                    // Inject only the visual labels (left side) into the active ComfyUI list
                    comboWidget.options.values = displayLabels;
                    
                    // Re-evaluate active value state
                    if (displayLabels.length > 0 && !displayLabels.includes(comboWidget.value)) {
                        comboWidget.value = displayLabels[0];
                    }
                    
                    if (node.graph) node.setDirtyCanvas(true, true);
                };

                // Intercept data submission: swap the visible UI label with the hidden output value
                comboWidget.serializeValue = function () {
                    const currentLabel = comboWidget.value;
                    if (!currentLabel) return "";
                    
                    // Extract the right-side value from the registry map, fallback to label if unmapped
                    return comboWidget.customValueMap?.[currentLabel] ?? currentLabel;
                };

                const originalCallback = listWidget.callback;
                listWidget.callback = function (value) {
                    updateComboOptions(value);
                    if (originalCallback) originalCallback.apply(this, arguments);
                };

                updateComboOptions(listWidget.value);
            }
        }
    }
});