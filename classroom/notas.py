"""
Carlos A Delgado
06 jun 2024
Script para calcular notas autograder
"""

import pandas as pd
import numpy as np 

repo = pd.read_csv("repositorio.csv")
grades = pd.read_csv("grades.csv")

repo.rename(columns={"Q00_User github": "github_username"},inplace=True)

repo_grades = pd.merge(repo, grades, on="github_username")

repo_save = repo_grades[["Nombre completo","Nombre de usuario","github_username","points_awarded","points_available"]].copy()

repo_save.loc[:, "nota"] = 5 * repo_save["points_awarded"] / repo_save["points_available"]

repo_save.to_csv("notas.csv")
