#!/usr/bin/python3

import pandas as pd

testing_account = 'lutetium.helen@gmail.com'

split_mcs = lambda x: pd.Series([i for i in reversed(x.split(' , '))])


def process_clothing(df, clothing_df, materials_df):
    df = df.drop(
        columns=['Creation Date', 'Modified Date', 'Creator', 'unique id'])
    # There is a dummy user who has 5 materials entered.
    df[['mc1', 'mc2', 'mc3', 'mc4', 'mc5']] = df[
        'material-and-content'].str.split(pat=' , ', expand=True)
    df = df.drop(
        columns=['material-and-content'])

    # bottoms joined clothing
    bjc = df.set_index('clothing').join(clothing_df.set_index('unique id'))

    # bottoms joined clothing joined materials
    bjcjm = bjc
    for i in range(1, 6):
        col = "mc" + str(i)
        bjcjm = bjcjm.set_index(col).join(
            materials_df.set_index('unique id'), rsuffix=i)
    return bjcjm[bjcjm['user-email'] != testing_account]

def write_shirts(clothing_df, materials_df):
    bottoms_df = pd.read_csv('raw_shirts.csv')
    process_clothing(bottoms_df, clothing_df, materials_df).to_csv(
        r'./shirts.csv', index=False, header=True)

def write_bottoms(clothing_df, materials_df):
    bottoms_df = pd.read_csv('raw_bottoms.csv')
    process_clothing(bottoms_df, clothing_df, materials_df).to_csv(
        r'./bottoms.csv', index=False, header=True)

def write_undergarments(clothing_df, materials_df):
    bottoms_df = pd.read_csv('raw_undergarments.csv')
    process_clothing(bottoms_df, clothing_df, materials_df).to_csv(
        r'./undergarments.csv', index=False, header=True)

def write_jackets(clothing_df, materials_df):
    bottoms_df = pd.read_csv('raw_jackets.csv')
    process_clothing(bottoms_df, clothing_df, materials_df).to_csv(
        r'./jackets.csv', index=False, header=True)

def main():

    clothing_df = pd.read_csv('raw_clothing.csv').drop(
        columns=['Creation Date', 'Modified Date', 'Creator'])
    materials_df = pd.read_csv('raw_materialandpercentage.csv').drop(
        columns=['Creation Date', 'Modified Date', 'Creator'])

    write_shirts(clothing_df, materials_df)
    write_bottoms(clothing_df, materials_df)
    write_undergarments(clothing_df, materials_df)
    write_jackets(clothing_df, materials_df)

if __name__ == '__main__':
    main()
