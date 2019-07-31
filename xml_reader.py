import pandas as pd

def xml_root_to_df(node, df=pd.DataFrame()):
    if df.empty:
        df = pd.DataFrame(
            {
                "Notice": [
                    "Please pass a dataframe with a starting column to this function"
                ]
            }
        )
    for child in node:
        # If the child node has further children descend into the tree
        if len(child) > 0:
            df = xml_root_to_df(child, df)
        # Otherwise if the node has text enter it into the row if the column data for that row is empty
        # If it already has data, null the column for that row and every column after it
        elif child.text is not None:
            # Make sure we have a column for the tag
            if child.tag not in df.columns:
                df[child.tag] = ["" for n in df.iterrows()]
            # If row value is NaN fill value with child text
            if pd.isna(df.iloc[-1][child.tag]) or df.iloc[-1][child.tag] == "":
                col_index = df.columns.get_loc(child.tag)
                df.iat[-1, col_index] = child.text
            else:
                new_row = copy.deepcopy(df.iloc[-1])
                col_index = df.columns.get_loc(child.tag)
                max_index = len(df.columns)
                for i in range(col_index, max_index):
                    new_row.iat[i] = pd.np.NaN
                new_row[child.tag] = child.text
                df = df.append(new_row)
    return df
