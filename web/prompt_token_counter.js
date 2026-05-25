import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

// Helper function to determine the dynamic background and text colors safely
function getTokenStyles(count) {
    if (count <= 65) {
        return { bgColor: "#0d3a19", textColor: "#00ffaa" }; // Safe zone: Deep Green
    } else if (count <= 75) {
        return { bgColor: "#4a420d", textColor: "#ffee00" }; // Warning zone: Deep Yellow
    } else {
        return { bgColor: "#4a0d0d", textColor: "#ff5555" }; // Danger zone: Deep Red
    }
}

// Global listener to capture backend execution signals and dispatch to the specific target node
api.addEventListener("text_driven_token_count_update", (event) => {
    const detail = event.detail;
    if (!detail || !detail.node_id) return;

    const targetNode = app.graph.getNodeById(parseInt(detail.node_id));
    if (targetNode) {
        const displayWidget = targetNode.widgets.find(w => w.name === "token_count_display");
        if (displayWidget) {
            displayWidget.value = detail.count;
            targetNode.setDirtyCanvas(true, true); // Force UI refresh to repaint colors instantly
        }
    }
});

app.registerExtension({
    name: "ComfyUI-Text-Driven-Workflows.PromptTokenCounter",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "TextDrivenPromptTokenCounter") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                const self = this;
                
                // Append the specialized read-only counter widget
                const displayWidget = self.addWidget("text", "token_count_display", "2", null, { serialize: false });
                
                if (displayWidget) {
                    displayWidget.label = "Token"; 
                    displayWidget.value = "2";
                    
                    // Directly paint the container and traffic-light colors onto the node canvas area
                    displayWidget.draw = function(ctx, node, widget_width, y, margin) {
                        const count = parseInt(this.value) || 0;
                        const styles = getTokenStyles(count);

                        // Paint the container background box
                        ctx.fillStyle = styles.bgColor;
                        ctx.fillRect(margin, y, widget_width - margin * 2, LiteGraph.NODE_WIDGET_HEIGHT);

                        // Render the clean English label text
                        ctx.fillStyle = "#ffffff";
                        ctx.font = "12px Arial";
                        ctx.fillText(this.label || this.name, margin + 10, y + LiteGraph.NODE_WIDGET_HEIGHT * 0.7);

                        // Render the right-aligned dynamic counter token integer
                        ctx.fillStyle = styles.textColor;
                        ctx.font = "bold 14px monospace";
                        ctx.textAlign = "right";
                        ctx.fillText(this.value, widget_width - margin - 10, y + LiteGraph.NODE_WIDGET_HEIGHT * 0.7);
                        ctx.textAlign = "left"; // Restore canvas context behavior
                    };
                }
                
                if (self.computeSize) {
                    self.setSize(self.computeSize());
                }
                
                return r;
            };
        }
    }
});