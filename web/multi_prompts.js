import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "ComfyUI-Text-Driven-Workflows.MultiPromptsTextDriven",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "TextDrivenMultiPrompts") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                const self = this;
                
                // Function to toggle visibility and layout based on selected slot count
                self.updateWidgets = function() {
                    const numWidget = self.widgets.find(w => w.name === "num_prompts");
                    if (!numWidget) return;
                    
                    const num = parseInt(numWidget.value, 10);
                    
                    for (let i = 1; i <= 10; i++) {
                        const show = i <= num;
                        const textWidget = self.widgets.find(w => w.name === `text_${i}`);
                        const multWidget = self.widgets.find(w => w.name === `multiplier_${i}`);
                        const actWidget = self.widgets.find(w => w.name === `active_${i}`);
                        
                        const toggleWidget = (w, show) => {
                            if (!w) return;
                            if (show) {
                                if (w.type === "hidden") {
                                    w.type = w.origType || "customtext";
                                    
                                    // FIXED: Re-instated the critical property deletion to restore prototype logic for standard widgets
                                    if (w.origComputeSize) {
                                        w.computeSize = w.origComputeSize;
                                    } else {
                                        delete w.computeSize;
                                    }
                                    
                                    if (w.origDraw) {
                                        w.draw = w.origDraw;
                                    } else {
                                        delete w.draw;
                                    }
                                }
                                if (w.inputEl) w.inputEl.style.display = "";
                                if (w.element) w.element.style.display = "";
                            } else {
                                if (w.type !== "hidden") {
                                    w.origType = w.type;
                                    w.origComputeSize = w.computeSize;
                                    w.origDraw = w.draw;
                                    
                                    w.type = "hidden";
                                    w.computeSize = () => [0, -4];
                                    w.draw = () => {}; 
                                }
                                if (w.inputEl) w.inputEl.style.display = "none";
                                if (w.element) w.element.style.display = "none";
                            }
                        };
                        
                        toggleWidget(textWidget, show);
                        toggleWidget(multWidget, show);
                        toggleWidget(actWidget, show);
                    }
                    
                    // Collapse node height dynamically to fit the current UI state
                    self.setSize(self.computeSize());
                    app.graph.setDirtyCanvas(true, true);
                };

                // Inject visibility updates into the dropdown callback
                const numWidget = self.widgets.find(w => w.name === "num_prompts");
                if (numWidget) {
                    const origCallback = numWidget.callback;
                    numWidget.callback = (value) => {
                        if (origCallback) origCallback(value);
                        self.updateWidgets();
                    };
                }

                // Apply initial UI shrinking for the default value (3) on creation
                setTimeout(() => self.updateWidgets(), 10);

                return r;
            };
            
            // Re-apply layout adjustment when loading saved workflows
            const onConfigure = nodeType.prototype.onConfigure;
            nodeType.prototype.onConfigure = function (info) {
                const r = onConfigure ? onConfigure.apply(this, [info]) : undefined;
                this.updateWidgets();
                return r;
            };
        }
    }
});