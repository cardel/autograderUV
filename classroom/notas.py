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

repo.loc[:,"github_username"] = repo['github_username'].map(lambda x: str.lower(x))
grades.loc[:,"github_username"] = grades['github_username'].map(lambda x: str.lower(x))

repo_grades = pd.merge(repo, grades, on="github_username")

repo_save = repo_grades[["Nombre completo","Nombre de usuario","github_username","points_awarded","points_available"]].copy()

repo_save.loc[:, "nota"] = 5 * repo_save["points_awarded"] / repo_save["points_available"]
repo_save.sort_values("Nombre completo", ascending=True, inplace=True)
repo_save.to_csv("notas.csv")

#Mostrar estudiantes que no aparecen en el repositorio

no_match_repo = repo[~repo["github_username"].isin(repo_grades["github_username"])].copy()

print(no_match_repo[["Nombre completo","Nombre de usuario","github_username"]])
