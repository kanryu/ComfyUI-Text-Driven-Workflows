import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "TextDrivenWorkflows.ResolutionSelector", // 拡張機能の登録名を変更
    async nodeCreated(node) {
        if (node.comfyClass === "TextDrivenResolutionSelector") { // 新しいノードIDをターゲットにする
            const listWidget = node.widgets.find(w => w.name === "resolutions_list");
            const comboWidget = node.widgets.find(w => w.name === "selected_resolution");

            if (listWidget && comboWidget) {
                const updateComboOptions = (textValue) => {
                    if (!textValue) return;
                    
                    // Split the text block into individual rows
                    const lines = textValue.split("\n")
                        .map(line => line.trim())
                        .filter(line => line.length > 0);
                    
                    // ComfyUI renders whatever is inside options.values.
                    // We feed the full human-readable string directly to the UI.
                    comboWidget.options.values = lines;
                    
                    if (lines.length > 0 && !lines.includes(comboWidget.value)) {
                        comboWidget.value = lines[0];
                    }
                    
                    if (node.graph) node.setDirtyCanvas(true, true);
                };

                // ★核心：表示を汚さず、サーバー送信時のみデータを「システム用の値」に化けさせる
                comboWidget.serializeValue = function () {
                    const currentValue = comboWidget.value;
                    if (!currentValue) return "";
                    
                    // Split by space as instructed, and send only the first token (e.g., "768x1024") to Python
                    const parts = currentValue.split(" ");
                    return parts[0].toLowerCase();
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