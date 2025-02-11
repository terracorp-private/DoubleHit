#!/usr/bin/env python

import pandas as pd
import sys 


def merger():

    df_onco = pd.read_csv(sys.argv[1], sep="\t")
    df_gen = pd.read_csv(sys.argv[2], sep="\t")

    df_gen.columns = ["Gene_Symbol",
                      "transcript",
                      "chromosome",
                      "-",
                      "-",
                      "-",
                      "-",
                      "-",
                      "-",
                      "-",
                      "-",
                      ]


    df_res = df_gen.merge(df_onco, on="Gene_Symbol", how="inner")
    df_res = df_res.iloc[:,:11]

    return df_res


print(merger().head())
merger().to_csv("../datasets/CNVkit_Dash_Data/Onco_genes.csv",
                index=False,
                header=False,
                sep="\t")


