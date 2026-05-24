import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "ComfyUI-Text-Driven-Workflows.TextLinePrompt",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "TextDrivenTextLinePrompt") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                const self = this;
                self.is_updating_widgets = false;
                
                const textWidget = self.widgets.find(w => w.name === "text");
                const comboWidget = self.widgets.find(w => w.name === "selected_line");
                const multWidget = self.widgets.find(w => w.name === "multiplier");
                const actWidget = self.widgets.find(w => w.name === "active");
                
                // Helper to safely extract the actual textarea DOM element across different ComfyUI V3 structures
                const getTextareaElement = (w) => {
                    if (!w) return null;
                    if (w.inputEl) return w.inputEl;
                    if (w.element) {
                        if (w.element.tagName === "TEXTAREA") return w.element;
                        return w.element.querySelector("textarea");
                    }
                    return null;
                };
                
                // Helper to cleanly deconstruct a line into semantic metadata components
                const parseLine = (line) => {
                    let trimmed = line.trim();
                    const active = !trimmed.startsWith("//");
                    let content = active ? trimmed : trimmed.replace(/^\s*\/\//, "").trim();
                    
                    content = content.replace(/,\s*$/, "").trim();
                    
                    let label = "";
                    let prompt = "";
                    if (content.includes("|-|")) {
                        const parts = content.split("|-|");
                        label = parts[0].trim();
                        prompt = parts.slice(1).join("|-|").trim();
                    } else {
                        label = content;
                        prompt = content;
                    }
                    
                    const unescapedOpenCount = (prompt.match(/(?<!\\)\(/g) || []).length;
                    
                    let multiplier = 1.0;
                    let isMultiParentheses = unescapedOpenCount >= 2;
                    
                    if (!isMultiParentheses && unescapedOpenCount === 1) {
                        const multMatch = prompt.match(/^\((.*):(\d+(?:\.\d+)?)\)$/);
                        if (multMatch) {
                            const innerContent = multMatch[1];
                            const innerUnescapedCount = (innerContent.match(/(?<!\\)\(/g) || []).length;
                            if (innerUnescapedCount === 0) {
                                prompt = innerContent.trim();
                                multiplier = parseFloat(multMatch[2]);
                            } else {
                                isMultiParentheses = true;
                            }
                        }
                    }
                    
                    return { active, label, prompt, multiplier, isMultiParentheses };
                };
                
                // Parse text block and dynamically populate combobox options list
                self.updateComboOptions = function() {
                    if (!textWidget || !comboWidget) return;
                    
                    const textValue = textWidget.value || "";
                    const lines = textValue.split("\n");
                    const options = [];
                    
                    lines.forEach((line, index) => {
                        if (line.trim() === "") return;
                        const { active, label } = parseLine(line);
                        const prefix = active ? "" : "// ";
                        options.push(`${index + 1}: ${prefix}${label || "(Empty)"}`);
                    });
                    
                    if (options.length === 0) options.push("none");
                    
                    const currentVal = comboWidget.value;
                    comboWidget.options.values = options;
                    
                    if (options.includes(currentVal)) {
                        comboWidget.value = currentVal;
                    } else {
                        // Trace and lock onto the row index prefix (e.g. '3:') to ensure robust follow-through when strings mutate
                        const match = currentVal ? currentVal.match(/^(\d+):/) : null;
                        if (match) {
                            const prefix = `${match[1]}:`;
                            const found = options.find(v => v.startsWith(prefix));
                            if (found) {
                                comboWidget.value = found;
                                return;
                            }
                        }
                        comboWidget.value = options[0];
                    }
                };
                
                // Read row string data and update standalone UI widgets values
                self.syncWidgetsFromSelectedLine = function() {
                    if (self.is_updating_widgets || !textWidget || !comboWidget || !multWidget || !actWidget) return;
                    
                    const selected = comboWidget.value;
                    if (!selected || selected === "none") return;
                    
                    const match = selected.match(/^(\d+):/);
                    if (!match) return;
                    
                    const lineIndex = parseInt(match[1], 10) - 1;
                    const lines = (textWidget.value || "").split("\n");
                    if (lineIndex < 0 || lineIndex >= lines.length) return;
                    
                    const { active, multiplier, isMultiParentheses } = parseLine(lines[lineIndex]);
                    
                    self.is_updating_widgets = true;
                    multWidget.value = isMultiParentheses ? 1.0 : multiplier;
                    actWidget.value = active;
                    self.is_updating_widgets = false;
                    
                    app.graph.setDirtyCanvas(true, false);
                };
                
                // Directly rewrite rows within the multiline element when controls trigger
                self.updateTextFromControls = function() {
                    if (self.is_updating_widgets || !textWidget || !comboWidget || !multWidget || !actWidget) return;
                    
                    const selected = comboWidget.value;
                    if (!selected || selected === "none") return;
                    
                    const match = selected.match(/^(\d+):/);
                    if (!match) return;
                    
                    const lineIndex = parseInt(match[1], 10) - 1;
                    const lines = (textWidget.value || "").split("\n");
                    if (lineIndex < 0 || lineIndex >= lines.length) return;
                    
                    const { label, prompt, isMultiParentheses } = parseLine(lines[lineIndex]);
                    const newActive = actWidget.value;
                    let newMultiplier = parseFloat(multWidget.value);
                    
                    // Scope isolation turned on immediately before firing dispatch events to safely block feedback loops
                    self.is_updating_widgets = true;
                    
                    if (isMultiParentheses) {
                        newMultiplier = 1.0;
                        multWidget.value = 1.0;
                    }
                    
                    let promptPart = prompt;
                    if (!isMultiParentheses && newMultiplier !== 1.0) {
                        // Convert to string via parseFloat to automatically drop trailing zeros (e.g., 1.10 -> 1.1)
                        const formattedMultiplier = parseFloat(newMultiplier.toFixed(2)).toString();
                        promptPart = `(${prompt}:${formattedMultiplier})`;
                    }
                    
                    const hasTrailingComma = lines[lineIndex].trim().endsWith(",");
                    let newLine = lines[lineIndex].includes("|-|") ? `${label}|-|${promptPart}` : promptPart;
                    
                    if (hasTrailingComma) {
                        newLine = `${newLine},`;
                    }
                    
                    if (!newActive) {
                        newLine = `//${newLine}`;
                    }
                    
                    lines[lineIndex] = newLine;
                    const newTextValue = lines.join("\n");
                    
                    textWidget.value = newTextValue;
                    if (textWidget.callback) {
                        textWidget.callback(newTextValue);
                    }
                    
                    const textarea = getTextareaElement(textWidget);
                    if (textarea) {
                        textarea.value = newTextValue;
                        textarea.dispatchEvent(new Event("input", { bubbles: true }));
                        textarea.dispatchEvent(new Event("change", { bubbles: true }));
                    }
                    
                    self.updateComboOptions();
                    const updatedSelected = comboWidget.options.values.find(v => v.startsWith(`${lineIndex + 1}:`));
                    if (updatedSelected) comboWidget.value = updatedSelected;
                    
                    // Release scope guard only after dropdown re-selection completes flawlessly
                    self.is_updating_widgets = false;
                    
                    app.graph.setDirtyCanvas(true, true);
                };
                
                setTimeout(() => {
                    const textarea = getTextareaElement(textWidget);
                    if (textarea) {
                        textarea.addEventListener("input", () => {
                            if (!self.is_updating_widgets) {
                                self.updateComboOptions();
                                self.syncWidgetsFromSelectedLine();
                            }
                        });
                    }
                }, 100);
                
                if (comboWidget) {
                    const origComboCallback = comboWidget.callback;
                    comboWidget.callback = function (value) {
                        if (origComboCallback) origComboCallback.call(this, value);
                        self.syncWidgetsFromSelectedLine();
                    };
                }
                
                if (multWidget) {
                    const origMultCallback = multWidget.callback;
                    multWidget.callback = function (value) {
                        if (origMultCallback) origMultCallback.call(this, value);
                        self.updateTextFromControls();
                    };
                }
                
                if (actWidget) {
                    const origActCallback = actWidget.callback;
                    actWidget.callback = function (value) {
                        if (origActCallback) origActCallback.call(this, value);
                        self.updateTextFromControls();
                    };
                }
                
                setTimeout(() => {
                    self.updateComboOptions();
                    self.syncWidgetsFromSelectedLine();
                }, 30);
                
                return r;
            };
            
            const onConfigure = nodeType.prototype.onConfigure;
            nodeType.prototype.onConfigure = function (info) {
                const r = onConfigure ? onConfigure.apply(this, [info]) : undefined;
                if (this.updateComboOptions) this.updateComboOptions();
                return r;
            };
        }
    }
});