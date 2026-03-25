/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onWillStart } from "@odoo/owl";

// ─── Einzelnes Feld (Text / Image / Selection) ───────────────────────────────
class TreeField extends Component {
    static template = "plant.TreeField";
    static props = ["field", "onSave"];

    setup() {
        this.state = useState({ editing: false });
        this.orm = useService("orm");
    }

    startEdit() {
        this.state.editing = true;
    }

    onKeydown(ev) {
        if (ev.key === "Enter") this.saveText(ev);
        if (ev.key === "Escape") this.state.editing = false;
    }

    // ── TEXT: Optimistic Update ───────────────────────────────────────────────
    async saveText(ev) {
        const val = ev.target.value;

        // 1. Sofort UI updaten
        this.props.field.value_text = val;
        this.state.editing = false;

        // 2. Im Hintergrund speichern — kein loadTree()!
        await this.orm.write("plant.field", [this.props.field.id], {
            value_text: val,
        });
    }

    // ── SELECTION: Optimistic Update ─────────────────────────────────────────
    async saveSelection(ev) {
        const val = parseInt(ev.target.value) || false;

        // Passende Option im lokalen Array finden
        const selectedOpt = this.props.field.selectionOptions
            ? this.props.field.selectionOptions.find(o => o.id === val)
            : null;

        // 1. Sofort UI updaten
        this.props.field.value_selection = val;
        this.props.field.value_selection_name = selectedOpt ? selectedOpt.name : "";
        this.state.editing = false;

        // 2. Im Hintergrund speichern — kein loadTree()!
        await this.orm.write("plant.field", [this.props.field.id], {
            value_selection: val,
        });
    }

    // ── IMAGE: muss neu laden wegen Base64 ───────────────────────────────────
    async saveImage(ev) {
        const file = ev.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = async (e) => {
            const base64 = e.target.result.split(",")[1];

            // 1. Sofort UI updaten
            this.props.field.value_image = base64;

            // 2. Im Hintergrund speichern
            await this.orm.write("plant.field", [this.props.field.id], {
                value_image: base64,
            });
        };
        reader.readAsDataURL(file);
    }
}

// ─── Rekursiver Baum-Knoten ───────────────────────────────────────────────────
class TreeNode extends Component {
    static template = "plant.TreeNode";
    static props = ["node", "level", "onSave"];

    setup() {
        this.state = useState({ open: this.props.level < 2 });
    }

    toggle() {
        if (this.hasChildren) {
            this.state.open = !this.state.open;
        }
    }

    get hasChildren() {
        return this.props.node.children && this.props.node.children.length > 0;
    }
}
// Rekursion: nach Klassendefinition setzen
TreeNode.components = { TreeField, TreeNode };

// ─── Haupt-Widget ─────────────────────────────────────────────────────────────
export class PlantTreeWidget extends Component {
    static template = "plant.PlantTreeWidget";
    static props = ["record"];
    static components = { TreeNode };

    setup() {
        this.orm = useService("orm");
        this.state = useState({ tree: [], loading: true });

        onWillStart(async () => {
            await this.loadTree();
        });
    }

    async loadTree() {
        this.state.loading = true;
        const templateId = this.props.record.resId;

        // 1. Blöcke laden
        const blocks = await this.orm.searchRead(
            "plant.block",
            [["template_id", "=", templateId]],
            ["id", "name", "aggregate_ids"]
        );

        // 2. Aggregate laden
        for (const block of blocks) {
            block.children = await this.orm.searchRead(
                "plant.aggregate",
                [["block_id", "=", block.id]],
                ["id", "name", "type_ids"]
            );

            // 3. Typen laden
            for (const agg of block.children) {
                agg.children = await this.orm.searchRead(
                    "plant.type",
                    [["aggregate_id", "=", agg.id]],
                    ["id", "name", "field_ids"]
                );

                // 4. Felder laden
                for (const type of agg.children) {
                    type.children = await this.orm.searchRead(
                        "plant.field",
                        [["type_id", "=", type.id]],
                        ["id", "name", "field_type",
                         "value_text", "value_image",
                         "value_selection", "selection_ids"]
                    );

                    // 5. Selection-Optionen + Anzeigename laden
                    for (const field of type.children) {
                        field.children = [];

                        if (field.field_type === "selection") {
                            // Optionen laden
                            field.selectionOptions = await this.orm.searchRead(
                                "plant.selection",
                                [["field_id", "=", field.id]],
                                ["id", "name"]
                            );
                            // Anzeigename für aktuellen Wert setzen
                            if (field.value_selection) {
                                const current = field.selectionOptions.find(
                                    o => o.id === field.value_selection[0]
                                );
                                field.value_selection_name = current ? current.name : "";
                                field.value_selection = field.value_selection[0];
                            } else {
                                field.value_selection_name = "";
                                field.value_selection = false;
                            }
                        } else {
                            field.selectionOptions = [];
                        }
                    }
                }
            }
        }

        this.state.tree = blocks;
        this.state.loading = false;
    }

    // Wird nur noch für Image-Uploads gebraucht
    async onSave() {
        await this.loadTree();
    }
}

// Widget bei Odoo registrieren
registry.category("view_widgets").add("plant_tree_widget", {
    component: PlantTreeWidget,
});
