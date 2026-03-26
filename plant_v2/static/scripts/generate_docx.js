const {
    Document, Packer, Paragraph, TextRun, HeadingLevel,
    AlignmentType, LevelFormat, BorderStyle, PageBreak,
    ImageRun, WidthType, Table, TableRow, TableCell, ShadingType
} = require('docx');
const fs = require('fs');

// Daten aus Argument lesen
const data = JSON.parse(process.argv[2]);
const outputPath = process.argv[3];

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

const children = [];

// Titel
children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun({ text: data.name, bold: true })]
}));

children.push(new Paragraph({
    children: [new TextRun({ text: `Plant: ${data.plant_name}`, color: "666666", size: 22 })]
}));

children.push(new Paragraph({ children: [new PageBreak()] }));

// Blöcke
let blockNum = 0;
for (const block of data.blocks) {
    blockNum++;

    // Block = Heading 1
    children.push(new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun(`${blockNum}. ${block.name}`)]
    }));

    let aggNum = 0;
    for (const agg of block.aggregates) {
        aggNum++;

        // Aggregat = Heading 2
        children.push(new Paragraph({
            heading: HeadingLevel.HEADING_2,
            children: [new TextRun(`${blockNum}.${aggNum}. ${agg.name}`)]
        }));

        // Felder als Bullet Points
        for (const field of agg.fields) {
            if ((field.field_type === 'text' && field.value_text) ||
                (field.field_type === 'selection' && field.value_selection_name)) {

                const val = field.field_type === 'text'
                    ? field.value_text
                    : field.value_selection_name;

                children.push(new Paragraph({
                    numbering: { reference: "bullets", level: 0 },
                    children: [
                        new TextRun({ text: `${field.name}: `, bold: true }),
                        new TextRun(val)
                    ]
                }));
            }
        }

        // Bilder nebeneinander
        const images = agg.fields.filter(f => f.field_type === 'image' && f.value_image);
        if (images.length > 0) {
            children.push(new Paragraph({ children: [] })); // Leerzeile

            // Bilder in Tabelle nebeneinander
            const imgCells = images.map(img => {
                const imgBuffer = Buffer.from(img.value_image, 'base64');
                return new TableCell({
                    borders,
                    width: { size: Math.floor(9026 / Math.min(images.length, 2)), type: WidthType.DXA },
                    children: [new Paragraph({
                        children: [new ImageRun({
                            data: imgBuffer,
                            type: 'png',
                            transformation: { width: 200, height: 150 }
                        })]
                    })]
                });
            });

            // Max 2 Bilder pro Zeile
            for (let i = 0; i < imgCells.length; i += 2) {
                const row = imgCells.slice(i, i + 2);
                while (row.length < 2) {
                    row.push(new TableCell({
                        borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } },
                        width: { size: Math.floor(9026 / 2), type: WidthType.DXA },
                        children: [new Paragraph({ children: [] })]
                    }));
                }
                children.push(new Table({
                    width: { size: 9026, type: WidthType.DXA },
                    columnWidths: [4513, 4513],
                    rows: [new TableRow({ children: row })]
                }));
            }
        }

        // Seitenumbruch nach Aggregat
        children.push(new Paragraph({ children: [new PageBreak()] }));
    }
}

const doc = new Document({
    numbering: {
        config: [{
            reference: "bullets",
            levels: [{
                level: 0,
                format: LevelFormat.BULLET,
                text: "•",
                alignment: AlignmentType.LEFT,
                style: { paragraph: { indent: { left: 720, hanging: 360 } } }
            }]
        }]
    },
    styles: {
        default: { document: { run: { font: "Arial", size: 24 } } },
        paragraphStyles: [
            { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
              run: { size: 36, bold: true, font: "Arial", color: "1F3864" },
              paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0,
                border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "1F3864", space: 1 } } } },
            { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
              run: { size: 28, bold: true, font: "Arial", color: "2E75B6" },
              paragraph: { spacing: { before: 180, after: 120 }, outlineLevel: 1 } },
        ]
    },
    sections: [{
        properties: {
            page: {
                size: { width: 11906, height: 16838 },
                margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
            }
        },
        children
    }]
});

Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync(outputPath, buffer);
    console.log('OK');
});
