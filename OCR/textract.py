import boto3

def extract_table_from_bytes(image_bytes):
    textract = boto3.client('textract', region_name='us-east-1')

    response = textract.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['TABLES']
    )

    blocks = response['Blocks']
    block_map = {block['Id']: block for block in blocks}
    rows = []

    for block in blocks:
        if block['BlockType'] == 'TABLE':
            table_cells = [b for b in blocks if b['BlockType'] == 'CELL']
            if not table_cells:
                continue

            max_row = max(cell['RowIndex'] for cell in table_cells)
            max_col = max(cell['ColumnIndex'] for cell in table_cells)

            table = [['' for _ in range(max_col)] for _ in range(max_row)]

            for cell in table_cells:
                row_idx = cell['RowIndex'] - 1
                col_idx = cell['ColumnIndex'] - 1
                text = ''

                if 'Relationships' in cell:
                    for rel in cell['Relationships']:
                        if rel['Type'] == 'CHILD':
                            for child_id in rel['Ids']:
                                word = block_map[child_id]
                                if word['BlockType'] == 'WORD':
                                    text += word['Text'] + ' '

                table[row_idx][col_idx] = text.strip()

            rows.extend(table)

    return rows



def extract_all_text(image_bytes):
    textract = boto3.client('textract', region_name='us-east-1')

    response = textract.detect_document_text(
        Document={'Bytes': image_bytes}
    )

    lines = []
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            lines.append(block['Text'])

    return lines
