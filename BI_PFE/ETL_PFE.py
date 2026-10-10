import pandas as pd
import psycopg2
from datetime import datetime

# Extraction

# Lecture du fichier Excel v_detail_engagement
de = pd.read_excel(r"C:\Users\fassa\Desktop\BI_PFE\v_detail_engagement.xls")
# Lecture du fichier Excel suivi_engagement_bud
ds = pd.read_excel(r"C:\Users\fassa\Desktop\BI_PFE\suivi_engagement_bud.xls")
# Lecture du fichier Excel Fournisseur
df = pd.read_excel(r"C:\Users\fassa\Desktop\BI_PFE\fournisseur.xls")
# Lecture du fichier Excel article_bdg
da = pd.read_excel(r"C:\Users\fassa\Desktop\BI_PFE\article_bdg.xls")
# Lecture du fichier Excel paragraphe
dp = pd.read_excel(r"C:\Users\fassa\Desktop\BI_PFE\s_paragraphe.xls")
# Lecture du fichier Excel commande_frn
dc = pd.read_excel(r"C:\Users\fassa\Desktop\BI_PFE\commande_frn.xls")
# Lecture du fichier Excel lig_commande_frn
dlc = pd.read_excel(r"C:\Users\fassa\Desktop\BI_PFE\lig_cmd_frn.xls")
# Lecture du fichier Excel fact_frn
dr = pd.read_excel(r"C:\Users\fassa\Desktop\BI_PFE\fact_frn.xls")
# Lecture du fichier Excel lig_fact_frn
dlf = pd.read_excel(r"C:\Users\fassa\Desktop\BI_PFE\lig_fact_frn.xls")
# Lecture du fichier Excel departement
dd = pd.read_excel(r"C:\Users\fassa\Desktop\BI_PFE\departement.xls")
# Lecture du fichier Excel famille
dfam = pd.read_excel(r"C:\Users\fassa\Desktop\BI_PFE\famille.xls")
# Lecture du fichier Excel sous_famille
dsfam = pd.read_excel(r"C:\Users\fassa\Desktop\BI_PFE\sous_famille.xls")
# Lecture du fichier Excel article
dart = pd.read_excel(r"C:\Users\fassa\Desktop\BI_PFE\article.xls")
# Lecture du fichier Excel titre
dt = pd.read_excel(r"C:\Users\fassa\Desktop\BI_PFE\titre.xls")
# Lecture du fichier Excel sous_titre
dst = pd.read_excel(r"C:\Users\fassa\Desktop\BI_PFE\sous_titres.xls")
# Lecture du fichier Excel chapitre
dch = pd.read_excel(r"C:\Users\fassa\Desktop\BI_PFE\chapitre.xls")

# Jointure entre sous_titre et titre
merged_dt = pd.merge(dst, dt[['COD_TIT', 'LIB_TIT']], on=['COD_TIT'], how='left')

# Jointure entre articleBUD et chapitre
merged_da = pd.merge(da, dch[['COD_CHAP', 'LIB_CHAP']], on=['COD_CHAP'], how='left')

# Jointure entre suivi_engagement_bud et paragraphe sur les colonnes 'cod_para' et 'cod_spara' (en conservant toutes les lignes de suivi_eng_bud)
merged_ds = pd.merge(ds, dp[['COD_PARA', 'COD_SPARA', 'LIB_SPARA']], on=['COD_PARA', 'COD_SPARA'], how='left')

# Jointure entre merged_ds et article_bdg sur les colonnes 'cod_art' et 'cod_chap' (en conservant toutes les lignes de merged_ds)
merged_ds = pd.merge(merged_ds, da[['COD_ART', 'COD_CHAP', 'LIB_ART', 'ETAT_ART']], on=['COD_ART', 'COD_CHAP'], how='left')

# Jointure entre v_detail_engagement et fournisseur sur la colonne 'cod_frn' (en conservant toutes les lignes de v_detail_engagement)
merged_df = pd.merge(de, df[['COD_FRN', 'NOM_FRN']], left_on='COD_TIER', right_on='COD_FRN', how='left')

# Jointure entre merged_df et paragraphe sur les colonnes 'cod_para' et 'cod_spara' (en conservant toutes les lignes de merged_df)
merged_df = pd.merge(merged_df, dp[['COD_PARA', 'COD_SPARA', 'LIB_SPARA']], on=['COD_PARA', 'COD_SPARA'], how='left')

# Jointure entre merged_df et article_bdg sur les colonnes 'cod_art' et 'cod_chap' (en conservant toutes les lignes de merged_df)
merged_df = pd.merge(merged_df, da[['COD_ART', 'COD_CHAP', 'LIB_ART', 'ETAT_ART']], on=['COD_ART', 'COD_CHAP'], how='left')

# Jointure entre commande_frn et fournisseur sur la colonne 'cod_frn' (en conservant toutes les lignes de commande_frn)
merged_dc = pd.merge(dc, df[['COD_FRN', 'NOM_FRN']], left_on='FRS_COD', right_on='COD_FRN', how='left')

# Effectuer une jointure à gauche en conservant toutes les lignes de merged_dc
merged_dc = pd.merge(merged_dc, dd[['ID_DEPT', 'DEP_NOM', 'DEP_NAT', 'ABRV']], on='ID_DEPT', how='left')

# Jointure entre fact_frn et fournisseur sur la colonne 'cod_frn' (en conservant toutes les lignes de fact_frn)
merged_dr = pd.merge(dr, df[['COD_FRN', 'NOM_FRN']], left_on='CODE_FRS_F', right_on='COD_FRN', how='left')

# Jointure entre fact_frn et departement sur la colonne 'id_dept' (en conservant toutes les lignes de fact_frn)
merged_dr = pd.merge(merged_dr, dd[['ID_DEPT', 'DEP_NOM','DEP_NAT','ABRV']], on='ID_DEPT', how='left')

# Jointure entre dlc,dlf et article sur les colonnes 'ART_COD' 
merged_dlc = pd.merge(dlc, dart[['ART_COD','COD_FAM',"SFAM_COD"]], on=['ART_COD'], how='left')
merged_dlf = pd.merge(dlf, dart[['ART_COD','COD_FAM',"SFAM_COD"]], on=['ART_COD'], how='left')

# Transformation

# Titre_ID
merged_df["COD_TIT"] = merged_df["COD_TIT"].fillna(0).astype(int)
merged_df["COD_STIT"] = merged_df["COD_STIT"].fillna(0).astype(int)

merged_dlf["COD_TIT"] = merged_dlf["COD_TIT"].fillna(0).astype(int)
merged_dlf["COD_STIT"] = merged_dlf["COD_STIT"].fillna(0).astype(int)

merged_ds["COD_TIT"] = merged_ds["COD_TIT"].fillna(0).astype(int)
merged_ds["COD_STIT"] = merged_ds["COD_STIT"].fillna(0).astype(int)

merged_dlc["COD_TIT"] = merged_dlc["COD_TIT"].fillna(0).astype(int)
merged_dlc["COD_STIT"] = merged_dlc["COD_STIT"].fillna(0).astype(int)

# Paragraphe_ID
merged_df["COD_PARA"] = merged_df["COD_PARA"].fillna(0).astype(int)
merged_df["COD_SPARA"] = merged_df["COD_SPARA"].fillna(0).astype(int)

merged_dlf["COD_PARA"] = merged_dlf["COD_PARA"].fillna(0).astype(int)
merged_dlf["COD_SPARA"] = merged_dlf["COD_SPARA"].fillna(0).astype(int)

merged_ds["COD_PARA"] = merged_ds["COD_PARA"].fillna(0).astype(int)
merged_ds["COD_SPARA"] = merged_ds["COD_SPARA"].fillna(0).astype(int)

merged_dlc["COD_PARA"] = merged_dlc["COD_PARA"].fillna(0).astype(int)
merged_dlc["COD_SPARA"] = merged_dlc["COD_SPARA"].fillna(0).astype(int)

# ArticleBUD_ID
merged_df["COD_CHAP"] = merged_df["COD_CHAP"].fillna(0).astype(int)
merged_df["COD_ART"] = merged_df["COD_ART"].fillna(0).astype(int)

merged_dlf["COD_CHAP"] = merged_dlf["COD_CHAP"].fillna(0).astype(int)
merged_dlf["COD_ART"] = merged_dlf["COD_ART"].fillna(0).astype(int)

merged_ds["COD_CHAP"] = merged_ds["COD_CHAP"].fillna(0).astype(int)
merged_ds["COD_ART"] = merged_ds["COD_ART"].fillna(0).astype(int)

merged_dlc["COD_CHAP"] = merged_dlc["COD_CHAP"].fillna(0).astype(int)
merged_dlc["COD_ART"] = merged_dlc["COD_ART"].fillna(0).astype(int)

# Dept_ID
merged_dlc["ID_DEPT"] = merged_dlc["ID_DEPT"].fillna(0).astype(int)

# Date_ID
merged_df["DAT_CMD"] = pd.to_datetime(merged_df["DAT_CMD"], errors="coerce", format="%d/%m/%Y")
merged_dlf["D_FACT"] = pd.to_datetime(merged_dlf["D_FACT"], errors="coerce", format="%d/%m/%Y")
merged_dlc["DAT_COM_FRN"] = pd.to_datetime(merged_dlc["DAT_COM_FRN"], errors="coerce", format="%d/%m/%Y")
merged_dr["D_FACT"] = pd.to_datetime(merged_dr["D_FACT"], errors="coerce", format="%d/%m/%Y")
merged_dc["DAT_COM_FRN"] = pd.to_datetime(merged_dc["DAT_COM_FRN"], errors="coerce", format="%d/%m/%Y")

# Remplacer les chanes vides par "0" dans les colonnes spécifiées
merged_df[['MNT_DEV','QTE_ENG', 'VAL_ENG', 'QTE_FACT', 'VAL_FACT', 'VAL_REG']] = merged_df[['MNT_DEV','QTE_ENG', 'VAL_ENG', 'QTE_FACT', 'VAL_FACT', 'VAL_REG']].fillna(0)
merged_ds[['PREVISION','V_ENG', 'V_FACT', 'V_REG']] = merged_ds[['PREVISION', 'V_ENG', 'V_FACT', 'V_REG']].fillna(0)
dc[['MT_TTC_ENG','MT_HT_ENG', 'MNT_TVA_ENG', 'MNT_REM_ENG', 'MNT_TAXE_ENG']] = dc[['MT_TTC_ENG','MT_HT_ENG', 'MNT_TVA_ENG', 'MNT_REM_ENG', 'MNT_TAXE_ENG']].fillna(0)
merged_dlc[["QTE_ART_CD","PU_ART_BRUT","PU_ART_CD","QTE_REST","MNT_TTC","MNT_HT","MNT_REM","MNT_TVA","MNT_TAX"]] = merged_dlc[["QTE_ART_CD","PU_ART_BRUT","PU_ART_CD","QTE_REST","MNT_TTC","MNT_HT","MNT_REM","MNT_TVA","MNT_TAX"]].fillna(0)
dr[['MNT_TTC_FAC','MNT_HT_FAC', 'MNT_TVA_FAC', 'MNT_REM_FAC', 'MNT_TAXE_FAC']] = dr[['MNT_TTC_FAC','MNT_HT_FAC', 'MNT_TVA_FAC', 'MNT_REM_FAC', 'MNT_TAXE_FAC']].fillna(0)
merged_dlf[["QTITE_ART_LIGF","PU_ART_LIGF","TAXE_ART_LIGF","REM_ART_LIGF","MNT_THT","MNT_TVA","MNT_REM"]] = merged_dlf[["QTITE_ART_LIGF","PU_ART_LIGF","TAXE_ART_LIGF","REM_ART_LIGF","MNT_THT","MNT_TVA","MNT_REM"]].fillna(0)


con=psycopg2.connect(dbname='PFE',user='postgres',password='admin')   
cursor = con.cursor()
cursor.execute("SET search_path TO PFE")


# Chargement

# Insertion des données dans la table dim_titre
for index, row in merged_dt.iterrows():
    titre = str(int(row["COD_TIT"]))
    stitre = str(int(row["COD_STIT"]))
    titre_id = f"{titre}/{stitre}"    
    cursor.execute("INSERT INTO dim_titre (titre_id, cod_titre, cod_stitre, lib_titre, lib_stitre) SELECT %s, %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_titre WHERE titre_id = %s)", (titre_id, row["COD_TIT"], row["COD_STIT"], row["LIB_TIT"], row["LIB_STIT"], titre_id))
for index, row in merged_df.iterrows():
    titre = str(int(row["COD_TIT"]))
    stitre = str(int(row["COD_STIT"]))
    titre_id = f"{titre}/{stitre}"    
    cursor.execute("INSERT INTO dim_titre (titre_id, cod_titre, cod_stitre, lib_titre, lib_stitre) SELECT %s, %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_titre WHERE titre_id = %s)", (titre_id, row["COD_TIT"], row["COD_STIT"], "--", "--", titre_id))
for index, row in merged_dlc.iterrows():
    titre = str(int(row["COD_TIT"]))
    stitre = str(int(row["COD_STIT"]))  
    titre_id = f"{titre}/{stitre}"    
    cursor.execute("INSERT INTO dim_titre (titre_id, cod_titre, cod_stitre, lib_titre, lib_stitre) SELECT %s, %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_titre WHERE titre_id = %s)", (titre_id, row["COD_TIT"], row["COD_STIT"], "--", "--", titre_id))
for index, row in merged_dlf.iterrows():
    titre = str(int(row["COD_TIT"]))
    stitre = str(int(row["COD_STIT"]))  
    titre_id = f"{titre}/{stitre}"    
    cursor.execute("INSERT INTO dim_titre (titre_id, cod_titre, cod_stitre, lib_titre, lib_stitre) SELECT %s, %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_titre WHERE titre_id = %s)", (titre_id, row["COD_TIT"], row["COD_STIT"], "--", "--", titre_id))
for index, row in merged_ds.iterrows():
    titre = str(int(row["COD_TIT"]))
    stitre = str(int(row["COD_STIT"]))  
    titre_id = f"{titre}/{stitre}"    
    cursor.execute("INSERT INTO dim_titre (titre_id, cod_titre, cod_stitre, lib_titre, lib_stitre) SELECT %s, %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_titre WHERE titre_id = %s)", (titre_id, row["COD_TIT"], row["COD_STIT"], "--", "--", titre_id))
print("success")


# Insertion des données dans la table dim_anneebud / dim_date
for index, row in merged_df.iterrows():
    cursor.execute("INSERT INTO dim_anneebud (annee_id, année) VALUES (%s, %s) ON CONFLICT DO NOTHING", (str(row["ANNEE"])[:4], str(row["ANNEE"])[:4]))
for index, row in merged_ds.iterrows():
    cursor.execute("INSERT INTO dim_anneebud (annee_id, année) VALUES (%s, %s) ON CONFLICT DO NOTHING", (str(row["ANNEE"])[:4], str(row["ANNEE"])[:4]))

for index, row in merged_df.iterrows():
    date_cmd = row["DAT_CMD"]
    if pd.notna(date_cmd):
        jour = date_cmd.day
        mois = date_cmd.month
        année = date_cmd.year
        date_id = datetime(année, mois, jour)
        cursor.execute("INSERT INTO dim_date (date_id, jour, mois, année) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING", (date_id, jour, mois, année))
for index, row in dc.iterrows():
    date_cmd = row["DAT_COM_FRN"]
    if pd.notna(date_cmd):
        jour = date_cmd.day
        mois = date_cmd.month
        année = date_cmd.year
        date_id = datetime(année, mois, jour)
        cursor.execute("INSERT INTO dim_date (date_id, jour, mois, année) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING", (date_id, jour, mois, année))
for index, row in dr.iterrows():
    date_cmd = row["D_FACT"]
    if pd.notna(date_cmd):
        jour = date_cmd.day
        mois = date_cmd.month
        année = date_cmd.year
        date_id = datetime(année, mois, jour)
        cursor.execute("INSERT INTO dim_date (date_id, jour, mois, année) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING", (date_id, jour, mois, année))
for index, row in dr.iterrows():
    date_cmd = row["DAT_COM_FRN"]
    if pd.notna(date_cmd):
        jour = date_cmd.day
        mois = date_cmd.month
        année = date_cmd.year
        date_id = datetime(année, mois, jour)
        cursor.execute("INSERT INTO dim_date (date_id, jour, mois, année) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING", (date_id, jour, mois, année))
for index, row in dlc.iterrows():
    date_cmd = row["DAT_COM_FRN"]
    if pd.notna(date_cmd):
        jour = date_cmd.day
        mois = date_cmd.month
        année = date_cmd.year
        date_id = datetime(année, mois, jour)
        cursor.execute("INSERT INTO dim_date (date_id, jour, mois, année) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING", (date_id, jour, mois, année))
for index, row in dlf.iterrows():
    date_cmd = row["D_FACT"]
    if pd.notna(date_cmd):
        jour = date_cmd.day
        mois = date_cmd.month
        année = date_cmd.year
        date_id = datetime(année, mois, jour)
        cursor.execute("INSERT INTO dim_date (date_id, jour, mois, année) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING", (date_id, jour, mois, année))
print("success")

# Insertion des données dans la table dim_article
for index, row in dart.iterrows():
    truncated_designation = str(row["DESIGNATION"])[:500]
    cursor.execute("INSERT INTO dim_article (article_id, cod_article, designation) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_article WHERE article_id = %s::varchar) ", (row["ART_COD"], row["ART_COD"], truncated_designation, row["ART_COD"]))
for index, row in merged_dlc.iterrows():
    cursor.execute("INSERT INTO dim_article (article_id, cod_article, designation) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_article WHERE article_id = %s::varchar)", (row["ART_COD"], row["ART_COD"], "--", row["ART_COD"]))
for index, row in merged_dlf.iterrows():
    cursor.execute("INSERT INTO dim_article (article_id, cod_article, designation) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_article WHERE article_id = %s::varchar)", (row["ART_COD"], row["ART_COD"], "--", row["ART_COD"]))

# Insertion des données dans la table dim_famille
for index, row in dfam.iterrows():
    cursor.execute("INSERT INTO dim_famille (famille_id, cod_famille, lib_famille, type) SELECT %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_famille WHERE famille_id = %s::varchar)", (row["COD_FAM"], row["COD_FAM"], row["FAM_LIB"], row["TYPE"], row["COD_FAM"]))
for index, row in merged_dlc.iterrows():
    cursor.execute("INSERT INTO dim_famille (famille_id, cod_famille, lib_famille, type) SELECT %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_famille WHERE famille_id = %s::varchar)", (row["COD_FAM"], row["COD_FAM"], "--", "--", row["COD_FAM"]))
for index, row in merged_dlf.iterrows():
    cursor.execute("INSERT INTO dim_famille (famille_id, cod_famille, lib_famille, type) SELECT %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_famille WHERE famille_id = %s::varchar)", (row["COD_FAM"], row["COD_FAM"], "--", "--", row["COD_FAM"]))


# Insertion des données dans la table dim_sfamille
for index, row in dsfam.iterrows():
    cursor.execute("INSERT INTO dim_sfamille (sfamille_id, cod_sfamille, lib_sfamille) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_sfamille WHERE sfamille_id = %s::varchar)", (row["SFAM_COD"], row["SFAM_COD"], row["SFAM_LIB"], row["SFAM_COD"]))
for index, row in merged_dlc.iterrows():
    cursor.execute("INSERT INTO dim_sfamille (sfamille_id, cod_sfamille, lib_sfamille) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_sfamille WHERE sfamille_id = %s::varchar)", (row["SFAM_COD"], row["SFAM_COD"], "--", row["SFAM_COD"]))
for index, row in merged_dlf.iterrows():
    cursor.execute("INSERT INTO dim_sfamille (sfamille_id, cod_sfamille, lib_sfamille) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_sfamille WHERE sfamille_id = %s::varchar)", (row["SFAM_COD"], row["SFAM_COD"], "--", row["SFAM_COD"]))

# Insertion des données dans la table dim_lig
for index, row in dlc.iterrows():
    cursor.execute("INSERT INTO dim_lig (lig_id, ligne) VALUES (%s, %s) ON CONFLICT DO NOTHING", (row["LIG"], row["LIG"]))
for index, row in dlf.iterrows():
    cursor.execute("INSERT INTO dim_lig (lig_id, ligne) VALUES (%s, %s) ON CONFLICT DO NOTHING", (row["LIG"], row["LIG"]))

# Insertion des données dans la table dim_Nat_Facture
for index, row in dr.iterrows():
    cursor.execute("INSERT INTO dim_nat_facture (nat_facture_id, nature_facture) VALUES (%s, %s) ON CONFLICT DO NOTHING", (row["NAT_FACT_FAC"], row["NAT_FACT_FAC"]))

# Insertion des données dans la table dim_SRC
for index, row in merged_df.iterrows():
    cursor.execute("INSERT INTO dim_src (src_id, src) VALUES (%s, %s) ON CONFLICT DO NOTHING", (row["SRC"], row["SRC"]))
print("success")

# Insertion des données dans la table dim_departement
for index, row in dd.iterrows():
    cursor.execute("INSERT INTO dim_departement (departement_id, nom_departement, abrv_departement, nat_departement) SELECT %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_departement WHERE departement_id = %s::varchar)", (row["ID_DEPT"], row["DEP_NOM"], row["ABRV"], row["DEP_NAT"], row["ID_DEPT"]))
for index, row in merged_dc.iterrows():
    cursor.execute("INSERT INTO dim_departement (departement_id, nom_departement, abrv_departement, nat_departement) SELECT %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_departement WHERE departement_id = %s::varchar)", (row["ID_DEPT"], "--", "--", "--", row["ID_DEPT"]))
for index, row in merged_dr.iterrows():
    cursor.execute("INSERT INTO dim_departement (departement_id, nom_departement, abrv_departement, nat_departement) SELECT %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_departement WHERE departement_id = %s::varchar)", (row["ID_DEPT"], "--", "--", "--", row["ID_DEPT"]))
for index, row in merged_dlc.iterrows():
    cursor.execute("INSERT INTO dim_departement (departement_id, nom_departement, abrv_departement, nat_departement) SELECT %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_departement WHERE departement_id = %s::varchar)", (row["ID_DEPT"], "--", "--", "--", row["ID_DEPT"]))
print("success")

# Insertion des données dans la table dim_type_cmd
for index, row in dc.iterrows():
    cursor.execute("INSERT INTO dim_type_cmd (type_cmd_id, type) VALUES (%s, %s) ON CONFLICT DO NOTHING", (row["TYP_CMD"], row["TYP_CMD"]))
for index, row in dr.iterrows():
    cursor.execute("INSERT INTO dim_type_cmd (type_cmd_id, type) VALUES (%s, %s) ON CONFLICT DO NOTHING", (row["TYP_CMD"], row["TYP_CMD"]))
print("success")

# Insertion des données dans la table dim_Engagement
for index, row in merged_df.iterrows():
    cursor.execute("INSERT INTO dim_engagement (eng_id, type_engagement) VALUES (%s, %s) ON CONFLICT DO NOTHING", (row["TYP_ENG"], row["TYP_ENG"]))
print("success")
# Insertion des données dans la table dim_commande_eng
for index, row in merged_df.iterrows():
    cursor.execute("INSERT INTO dim_commande_eng (commande_eng_id, num_commande_eng, num_ph, lib_commande_eng) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING", (row["NUM_CMD"], row["NUM_CMD"], row["NUM_PH"], row["LIB_CMD"]))

# Insertion des données dans la table dim_commande
for index, row in dc.iterrows():
    cursor.execute("INSERT INTO dim_commande (commande_id, num_commande) VALUES (%s, %s) ON CONFLICT DO NOTHING", (row["NUM_COM_FRN"], row["NUM_COM_FRN"]))
for index, row in dlc.iterrows():
    cursor.execute("INSERT INTO dim_commande (commande_id, num_commande) VALUES (%s, %s) ON CONFLICT DO NOTHING", (row["NUM_COM_FRN"], row["NUM_COM_FRN"]))

# Insertion des données dans la table dim_fournisseur
for index, row in df.iterrows():
    cursor.execute("INSERT INTO dim_fournisseur (fournisseur_id, cod_fournisseur, nom_fournisseur) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_fournisseur WHERE fournisseur_id = %s::varchar)", (row["COD_FRN"], row["COD_FRN"], row["NOM_FRN"], row["COD_FRN"]))
for index, row in merged_df.iterrows():
    cursor.execute("INSERT INTO dim_fournisseur (fournisseur_id, cod_fournisseur, nom_fournisseur) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_fournisseur WHERE fournisseur_id = %s::varchar)", (row["COD_TIER"], row["COD_TIER"], "--", row["COD_TIER"]))
for index, row in merged_dc.iterrows():
    cursor.execute("INSERT INTO dim_fournisseur (fournisseur_id, cod_fournisseur, nom_fournisseur) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_fournisseur WHERE fournisseur_id = %s::varchar)", (row["FRS_COD"], row["FRS_COD"], "--", row["FRS_COD"]))
for index, row in merged_dr.iterrows():
    cursor.execute("INSERT INTO dim_fournisseur (fournisseur_id, cod_fournisseur, nom_fournisseur) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_fournisseur WHERE fournisseur_id = %s::varchar)", (row["CODE_FRS_F"], row["CODE_FRS_F"], "--", row["CODE_FRS_F"]))
for index, row in merged_dlc.iterrows():
    cursor.execute("INSERT INTO dim_fournisseur (fournisseur_id, cod_fournisseur, nom_fournisseur) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_fournisseur WHERE fournisseur_id = %s::varchar)", (row["FRS_COD"], row["FRS_COD"], "--", row["FRS_COD"]))
for index, row in merged_dlf.iterrows():
    cursor.execute("INSERT INTO dim_fournisseur (fournisseur_id, cod_fournisseur, nom_fournisseur) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM dim_fournisseur WHERE fournisseur_id = %s::varchar)", (row["CODE_FRS_F"], row["CODE_FRS_F"], "--", row["CODE_FRS_F"]))
print("success")

# Insertion des données dans la table dim_paragraphe
for index, row in dp.iterrows():
    para = str(row["COD_PARA"])
    spara = str(row["COD_SPARA"])
    paragraphe_id = f"{para}/{spara}"
    cursor.execute("INSERT INTO dim_paragraphe (paragraphe_id, cod_para, cod_spara, lib_spara) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING", (paragraphe_id, row["COD_PARA"], row["COD_SPARA"], row["LIB_SPARA"]))
for index, row in merged_df.iterrows():
    para = str(row["COD_PARA"])
    spara = str(row["COD_SPARA"])
    paragraphe_id = f"{para}/{spara}"
    cursor.execute("INSERT INTO dim_paragraphe (paragraphe_id, cod_para, cod_spara, lib_spara) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING", (paragraphe_id, row["COD_PARA"], row["COD_SPARA"], row["LIB_SPARA"]))
for index, row in merged_ds.iterrows():
    para = str(row["COD_PARA"])
    spara = str(row["COD_SPARA"])
    paragraphe_id = f"{para}/{spara}"
    cursor.execute("INSERT INTO dim_paragraphe (paragraphe_id, cod_para, cod_spara, lib_spara) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING", (paragraphe_id, row["COD_PARA"], row["COD_SPARA"], row["LIB_SPARA"]))
for index, row in merged_dlc.iterrows():
    para = str(row["COD_PARA"])
    spara = str(row["COD_SPARA"])
    paragraphe_id = f"{para}/{spara}"
    cursor.execute("""
        INSERT INTO dim_paragraphe (paragraphe_id, cod_para, cod_spara, lib_spara)
        SELECT %s, %s, %s, %s
        WHERE NOT EXISTS (
            SELECT 1 FROM dim_paragraphe
            WHERE paragraphe_id = %s::varchar)""", (paragraphe_id, row["COD_PARA"], row["COD_SPARA"], "--", paragraphe_id))
for index, row in merged_dlf.iterrows():
    para = str(row["COD_PARA"])
    spara = str(row["COD_SPARA"])
    paragraphe_id = f"{para}/{spara}"
    cursor.execute("""
        INSERT INTO dim_paragraphe (paragraphe_id, cod_para, cod_spara, lib_spara)
        SELECT %s, %s, %s, %s
        WHERE NOT EXISTS (
            SELECT 1 FROM dim_paragraphe
            WHERE paragraphe_id = %s::varchar)""", (paragraphe_id, row["COD_PARA"], row["COD_SPARA"], "--", paragraphe_id))
print("success")

# Insertion des données dans la table dim_articleBUD
for index, row in merged_da.iterrows():
    art = str(row["COD_ART"])
    chap = str(row["COD_CHAP"])
    articlebud_id = f"{art}/{chap}"
    cursor.execute("""
        INSERT INTO dim_articlebud (articlebud_id, cod_art, cod_chap, lib_art, lib_chap, etat_art) 
        SELECT %s, %s, %s, %s, %s, %s 
        WHERE NOT EXISTS (
            SELECT 1 FROM dim_articlebud WHERE articlebud_id = %s::varchar
        )
    """, (articlebud_id, row["COD_ART"], row["COD_CHAP"], row["LIB_ART"], row["LIB_CHAP"], row["ETAT_ART"], articlebud_id))

for df in [merged_df, merged_dlc, merged_dlf, merged_ds]:
    for index, row in df.iterrows():
        art = str(row["COD_ART"])
        chap = str(row["COD_CHAP"])
        articlebud_id = f"{art}/{chap}"
        cursor.execute("""
            INSERT INTO dim_articlebud (articlebud_id, cod_art, cod_chap, lib_art, lib_chap, etat_art) 
            SELECT %s, %s, %s, %s, %s, %s 
            WHERE NOT EXISTS (
                SELECT 1 FROM dim_articlebud WHERE articlebud_id = %s::varchar
            )
        """, (articlebud_id, row["COD_ART"], row["COD_CHAP"], "--", "--", "--", articlebud_id))

# Insertion des données dans la table dim_facture
for index, row in dr.iterrows():
    cursor.execute("""
        INSERT INTO dim_facture (facture_id, cod_facture, num_facture, lib_facture) 
        SELECT %s, %s, %s, %s 
        WHERE NOT EXISTS (
            SELECT 1 FROM dim_facture WHERE facture_id = %s::varchar
        )
    """, (row["NUM_FACT"], row["NUM_FACT"], row["NUM_FA"], row["LIB_FACT"], row["NUM_FACT"]))

for index, row in dlf.iterrows():
    cursor.execute("""
        INSERT INTO dim_facture (facture_id, cod_facture, num_facture, lib_facture) 
        SELECT %s, %s, %s, %s 
        WHERE NOT EXISTS (
            SELECT 1 FROM dim_facture WHERE facture_id = %s::varchar
        )
    """, (row["NUM_FACT"], row["NUM_FACT"], "", "", row["NUM_FACT"]))

# Insertion des données dans la table fact_v_detail_engagement
for index, row in merged_df.iterrows():
    date_cmd = row["DAT_CMD"]
    if pd.notnull(date_cmd):
        jour = date_cmd.day
        mois = date_cmd.month
        année = date_cmd.year
        date_id = datetime(année, mois, jour)

    para = str(row["COD_PARA"])
    spara = str(row["COD_SPARA"])
    paragraphe_id = f"{para}/{spara}"

    titre = str(int(row["COD_TIT"]))
    stitre = str(int(row["COD_STIT"]))  
    titre_id = f"{titre}/{stitre}"    

    art = str(row["COD_ART"])
    chap = str(row["COD_CHAP"])
    articlebud_id = f"{art}/{chap}"

    # Insérer les données dans la table fact_v_eng
    cursor.execute("INSERT INTO fact_v_detail_engagement (fournisseur_id, annee_id, date_com_id ,commande_eng_id, eng_id, src_id, titre_id, articlebud_id, paragraphe_id, mnt_dev, qte_eng, val_eng, qte_fact, val_fact, val_reg) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (row["COD_TIER"], str(row["ANNEE"])[:4], date_id, row["NUM_CMD"], row["TYP_ENG"], row["SRC"],
                      titre_id, articlebud_id, paragraphe_id, float(row["MNT_DEV"]), float(row["QTE_ENG"]), float(row["VAL_ENG"]), row["QTE_FACT"], row["VAL_FACT"], row["VAL_REG"]))

for index, row in dc.iterrows():
    # Récupérer les identifiants de dimensions pour chaque ligne
    date_cmd = row["DAT_COM_FRN"]
    jour = date_cmd.day
    mois = date_cmd.month
    année = date_cmd.year
    date_id = datetime(année, mois, jour)

    # Insérer les données dans la table fact_commande_frn
    cursor.execute(
    "INSERT INTO fact_commande_frn (fournisseur_id, date_com_frn_id, commande_id, departement_id, type_cmd_id, mt_ttc_eng, mt_ht_eng, mnt_tva_eng, mnt_rem_eng, mnt_taxe_eng) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
    (row["FRS_COD"], date_id, row["NUM_COM_FRN"], row["ID_DEPT"], row["TYP_CMD"], row["MT_TTC_ENG"], row["MT_HT_ENG"], row["MNT_TVA_ENG"], row["MNT_REM_ENG"], row["MNT_TAXE_ENG"])
    )

for index, row in dr.iterrows():
    # Récupérer les identifiants de dimensions pour chaque ligne
    date_cmd = row["DAT_COM_FRN"]
    jour = date_cmd.day
    mois = date_cmd.month
    année = date_cmd.year
    date_id = datetime(année, mois, jour)

    date_fact = row["D_FACT"]
    jour_f = date_fact.day
    mois_f = date_fact.month
    année_f = date_fact.year
    date_id_f = datetime(année_f, mois_f, jour_f)

    # Insérer les données dans la table fact_facture_frn
    cursor.execute(
    "INSERT INTO fact_facture_frn (fournisseur_id, date_com_frn_id, date_facture_id, facture_id, departement_id, type_cmd_id, nat_facture_id, com_frn_id, mnt_ttc_fac, mnt_ht_fac, mnt_tva_fac, mnt_rem_fac, mnt_taxe_fac) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
    (row["CODE_FRS_F"], date_id, date_id_f, row["NUM_FACT"], row["ID_DEPT"], row["TYP_CMD"], row["NAT_FACT_FAC"], row["NUM_COM_FRN"], row["MNT_TTC_FAC"], row["MNT_HT_FAC"], row["MNT_TVA_FAC"], row["MNT_REM_FAC"], row["MNT_TAXE_FAC"])
    )


for index, row in merged_dlc.iterrows():
    # Récupérer les identifiants de dimensions pour chaque ligne
    date_cmd = row["DAT_COM_FRN"]
    jour = date_cmd.day
    mois = date_cmd.month
    année = date_cmd.year
    date_id = datetime(année, mois, jour)

    para = str(row["COD_PARA"])
    spara = str(row["COD_SPARA"])
    paragraphe_id = f"{para}/{spara}"

    titre = str(int(row["COD_TIT"]))
    stitre = str(int(row["COD_STIT"]))   
    titre_id = f"{titre}/{stitre}"

    art = str(row["COD_ART"])
    chap = str(row["COD_CHAP"])
    articlebud_id = f"{art}/{chap}"

    # Insérer les données dans la table lig_fact_commande_frn
    cursor.execute("INSERT INTO fact_lig_cmd_frn (fournisseur_id, date_com_frn_id, commande_id, departement_id, lig_id, article_id, famille_id, sfamille_id, titre_id, articlebud_id, paragraphe_id, qte_art_cd, pu_art_brut, pu_art_cd, qte_rest, mnt_ttc, mnt_ht, mnt_rem, mnt_tva, mnt_tax) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (row["FRS_COD"], date_id, row["NUM_COM_FRN"], row["ID_DEPT"], row["LIG"], row["ART_COD"], row["COD_FAM"], row["SFAM_COD"], titre_id, articlebud_id, paragraphe_id, row["QTE_ART_CD"], row["PU_ART_BRUT"], row["PU_ART_CD"], row["QTE_REST"], row["MNT_TTC"], row["MNT_HT"], row["MNT_REM"], row["MNT_TVA"], row["MNT_TAX"]))
print("success")

for index, row in merged_dlf.iterrows():
    # Récupérer les identifiants de dimensions pour chaque ligne
    date_cmd = row["D_FACT"]
    jour = date_cmd.day
    mois = date_cmd.month
    année = date_cmd.year
    date_id = datetime(année, mois, jour)

    para = str(row["COD_PARA"])
    spara = str(row["COD_SPARA"])
    paragraphe_id = f"{para}/{spara}"

    titre = str(int(row["COD_TIT"]))
    stitre = str(int(row["COD_STIT"]))  
    titre_id = f"{titre}/{stitre}"

    art = str(row["COD_ART"])
    chap = str(row["COD_CHAP"])
    articlebud_id = f"{art}/{chap}"

    # Insérer les données dans la table lig_fact_commande_frn
    cursor.execute("""
    INSERT INTO fact_lig_fact_frn 
    (fournisseur_id, date_fact_id, facture_id, lig_id, article_id, famille_id, sfamille_id, titre_id, articlebud_id, paragraphe_id, qtite_art_ligf, pu_art_ligf, taxe_art_ligf, rem_art_ligf, mnt_tht, mnt_tva, mnt_rem) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", (
    row["CODE_FRS_F"],date_id,row["NUM_FACT"],row["LIG"],row["ART_COD"],row["COD_FAM"],row["SFAM_COD"],titre_id,articlebud_id,paragraphe_id,row["QTITE_ART_LIGF"],
    row["PU_ART_LIGF"],row["TAXE_ART_LIGF"],row["REM_ART_LIGF"],row["MNT_THT"],row["MNT_TVA"],row["MNT_REM"]
))
    
for index, row in merged_ds.iterrows():
    para = str(row["COD_PARA"])
    spara = str(row["COD_SPARA"])
    paragraphe_id = f"{para}/{spara}"

    titre = str(int(row["COD_TIT"]))
    stitre = str(int(row["COD_STIT"]))  
    titre_id = f"{titre}/{stitre}"    

    art = str(row["COD_ART"])
    chap = str(row["COD_CHAP"])
    articlebud_id = f"{art}/{chap}"

    cursor.execute("""
    INSERT INTO fact_suivi_engagement_bud 
    (annee_id, titre_id, articlebud_id, paragraphe_id, prevision, v_eng, v_fact, v_reg) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""", (
    str(row["ANNEE"])[:4],
    titre_id,
    articlebud_id,
    paragraphe_id,
    row["PREVISION"],
    row["V_ENG"],
    row["V_FACT"],
    row["V_REG"]
))
    
print("success")
    
con.commit()
cursor.close()
con.close()