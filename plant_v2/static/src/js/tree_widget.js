/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onWillStart } from "@odoo/owl";

// ─── Einzelnes Feld (liest/schreibt plant.template.value) ────────────────────
class TreeField extends Component {
    static template = "plant.TreeField";
    static props = ["field", "onSave"];

    setup() {
        this.state = useState({ editing: false });
        this.orm = useService("orm");
    }

    startEdit() { this.state.editing = true; }

    onKeydown(ev) {
        if (ev.key === "Enter") this.saveText(ev);
        if (ev.key === "Escape") this.state.editing = false;
    }

    async saveText(ev) {
        const val = ev.target.value;
        this.props.field.value_text = val;
        this.state.editing = false;
        await this.orm.write("plant.template.value", [this.props.field.id], {
            value_text: val,
        });
    }

    async saveSelection(ev) {
        const val = parseInt(ev.target.value) || false;
        const selectedOpt = this.props.field.selectionOptions
            ? this.props.field.selectionOptions.find(o => o.id === val)
            : null;
        this.props.field.value_selection_id = val;
        this.props.field.value_selection_name = selectedOpt ? selectedOpt.name : "";
        this.state.editing = false;
        await this.orm.write("plant.template.value", [this.props.field.id], {
            value_selection_id: val,
        });
    }

    async saveImage(ev) {
        const file = ev.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = async (e) => {
            const base64 = e.target.result.split(",")[1];
            this.props.field.value_image = base64;
            await this.orm.write("plant.template.value", [this.props.field.id], {
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
        if (this.hasChildren) this.state.open = !this.state.open;
    }

    get hasChildren() {
        return this.props.node.children && this.props.node.children.length > 0;
    }
}
TreeNode.components = { TreeField, TreeNode };

// ─── Haupt-Widget ─────────────────────────────────────────────────────────────
export class PlantTreeWidget extends Component {
    static template = "plant.PlantTreeWidget";
    static props = ["record"];
    static components = { TreeNode };

    setup() {
        this.orm = useService("orm");
        this.state = useState({ tree: [], loading: true });
        onWillStart(async () => { await this.loadTree(); });
    }

    async loadTree() {
        // Noch nicht gespeichert — nichts laden
        if (!this.props.record.resId) {
            this.state.loading = false;
            return;
        }
        this.state.loading = true;
        const templateId = this.props.record.resId;

        // Alle Werte des Templates laden
        const values = await this.orm.searchRead(
            "plant.template.value",
            [["template_id", "=", templateId]],
            ["id", "field_id", "field_name", "field_type",
             "type_id", "aggregate_id", "block_id",
             "value_text", "value_image", "value_selection_id"]
        );

        // Blocks laden (für Namen + Reihenfolge)
        const template = await this.orm.read(
            "plant.template", [templateId], ["plant_id"]
        );
        const plantId = template[0].plant_id[0];

        const blocks = await this.orm.searchRead(
            "plant.block",
            [["plant_id", "=", plantId]],
            ["id", "name", "aggregate_ids"],
            { order: "id asc" }
        );

        // Baum aufbauen aus den geladenen Daten
        for (const block of blocks) {
            block.children = [];
            block.type = "block";

            const aggregates = await this.orm.searchRead(
                "plant.aggregate",
                [["block_id", "=", block.id]],
                ["id", "name", "type_ids"],
                { order: "id asc" }
            );

            for (const agg of aggregates) {
                agg.children = [];
                agg.type = "aggregate";

                const types = await this.orm.searchRead(
                    "plant.type",
                    [["aggregate_id", "=", agg.id]],
                    ["id", "name", "field_ids"],
                    { order: "id asc" }
                );

                for (const type of types) {
                    type.children = [];
                    type.type = "type";

                    // Felder = plant.template.value für diesen Typ
                    const typeValues = values.filter(
                        v => v.type_id && v.type_id[0] === type.id
                    );

                    for (const val of typeValues) {
                        val.children = [];
                        val.name = val.field_name;
                        val.type = "field";

                        // Selection Optionen laden
                        if (val.field_type === "selection") {
                            val.selectionOptions = await this.orm.searchRead(
                                "plant.selection",
                                [["field_id", "=", val.field_id[0]]],
                                ["id", "name"]
                            );
                            if (val.value_selection_id) {
                                const cur = val.selectionOptions.find(
                                    o => o.id === val.value_selection_id[0]
                                );
                                val.value_selection_name = cur ? cur.name : "";
                                val.value_selection_id = val.value_selection_id[0];
                            } else {
                                val.value_selection_name = "";
                                val.value_selection_id = false;
                            }
                        } else {
                            val.selectionOptions = [];
                        }
                        type.children.push(val);
                    }

                    if (type.children.length) agg.children.push(type);
                }

                if (agg.children.length) block.children.push(agg);
            }
        }

        this.state.tree = blocks.filter(b => b.children.length);
        this.state.loading = false;
    }

    async onSave() {
        await this.loadTree();
    }
}

registry.category("view_widgets").add("plant_tree_widget", {
    component: PlantTreeWidget,
});
