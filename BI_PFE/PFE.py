import psycopg2

con = psycopg2.connect(dbname='PFE', user='postgres', password='admin')
cur = con.cursor()

cur.execute('CREATE SCHEMA PFE')
cur.execute("SET search_path TO PFE")

# Create dimension tables
cur.execute('CREATE TABLE dim_Fournisseur (Fournisseur_ID VARCHAR(150), COD_Fournisseur VARCHAR(150), NOM_Fournisseur VARCHAR(150))')
cur.execute('ALTER TABLE dim_Fournisseur ADD CONSTRAINT pk_fournisseur PRIMARY KEY (Fournisseur_ID)')

cur.execute('CREATE TABLE dim_date (DATE_ID DATE, jour VARCHAR(2), mois VARCHAR(2), année VARCHAR(4))')
cur.execute('ALTER TABLE dim_date ADD CONSTRAINT pk_date PRIMARY KEY (DATE_ID)')

cur.execute('CREATE TABLE dim_anneebud (ANNEE_ID VARCHAR(4), année VARCHAR(4))')
cur.execute('ALTER TABLE dim_anneebud ADD CONSTRAINT pk_anneebud PRIMARY KEY (ANNEE_ID)')

cur.execute('CREATE TABLE dim_Commande_Eng (Commande_Eng_ID VARCHAR(150), NUM_Commande_Eng VARCHAR(150), NUM_PH VARCHAR(150), LIB_Commande_Eng VARCHAR(500))')
cur.execute('ALTER TABLE dim_Commande_Eng ADD CONSTRAINT pk_Commande_Eng PRIMARY KEY (Commande_Eng_ID)')

cur.execute('CREATE TABLE dim_Commande (Commande_ID VARCHAR(150), NUM_Commande VARCHAR(150))')
cur.execute('ALTER TABLE dim_Commande ADD CONSTRAINT pk_Commande PRIMARY KEY (Commande_ID)')

cur.execute('CREATE TABLE dim_Departement (Departement_ID VARCHAR(150), NOM_Departement VARCHAR(150), ABRV_Departement VARCHAR(150), NAT_Departement VARCHAR(150))')
cur.execute('ALTER TABLE dim_Departement ADD CONSTRAINT pk_Departement PRIMARY KEY (Departement_ID)')

cur.execute('CREATE TABLE dim_LIG (LIG_ID VARCHAR(150), Ligne VARCHAR(150))')
cur.execute('ALTER TABLE dim_LIG ADD CONSTRAINT pk_LIG PRIMARY KEY (LIG_ID)')

cur.execute('CREATE TABLE dim_Article (Article_ID VARCHAR(150), COD_Article VARCHAR(150), Designation VARCHAR(5000))')
cur.execute('ALTER TABLE dim_Article ADD CONSTRAINT pk_Article PRIMARY KEY (Article_ID)')

cur.execute('CREATE TABLE dim_Famille (Famille_ID VARCHAR(150), COD_Famille VARCHAR(150), LIB_Famille VARCHAR(150), Type VARCHAR(150))')
cur.execute('ALTER TABLE dim_Famille ADD CONSTRAINT pk_Famille PRIMARY KEY (Famille_ID)')

cur.execute('CREATE TABLE dim_SFamille (SFamille_ID VARCHAR(150), COD_SFamille VARCHAR(150), LIB_SFamille VARCHAR(150))')
cur.execute('ALTER TABLE dim_SFamille ADD CONSTRAINT pk_SFamille PRIMARY KEY (SFamille_ID)')

cur.execute('CREATE TABLE dim_Titre (Titre_ID VARCHAR(150), COD_Titre VARCHAR(150), COD_STitre VARCHAR(150), LIB_Titre VARCHAR(150), LIB_STitre VARCHAR(150))')
cur.execute('ALTER TABLE dim_Titre ADD CONSTRAINT pk_Titre PRIMARY KEY (Titre_ID)')

cur.execute('CREATE TABLE dim_ArticleBUD (ArticleBUD_ID VARCHAR(150), COD_Art VARCHAR(150), COD_Chap VARCHAR(150),LIB_Art VARCHAR(150), LIB_Chap VARCHAR(150), ETAT_Art VARCHAR(10))')
cur.execute('ALTER TABLE dim_ArticleBUD ADD CONSTRAINT pk_ArticleBUD PRIMARY KEY (ArticleBUD_ID)')

cur.execute('CREATE TABLE dim_Paragraphe (Paragraphe_ID VARCHAR(150), COD_Para VARCHAR(150), COD_SPara VARCHAR(150), LIB_SPara VARCHAR(150))')
cur.execute('ALTER TABLE dim_Paragraphe ADD CONSTRAINT pk_Paragraphe PRIMARY KEY (Paragraphe_ID)')

cur.execute('CREATE TABLE dim_Type_CMD (Type_CMD_ID VARCHAR(150), Type VARCHAR(150))')
cur.execute('ALTER TABLE dim_Type_CMD ADD CONSTRAINT pk_Type_CMD PRIMARY KEY (Type_CMD_ID)')

cur.execute('CREATE TABLE dim_Nat_Facture (Nat_Facture_ID VARCHAR(20), Nature_Facture VARCHAR(20))')
cur.execute('ALTER TABLE dim_Nat_Facture ADD CONSTRAINT pk_Nat_Facture PRIMARY KEY (Nat_Facture_ID)')

cur.execute('CREATE TABLE dim_Facture (Facture_ID VARCHAR(150), COD_Facture VARCHAR(150), NUM_Facture VARCHAR(150), LIB_Facture VARCHAR(500))')
cur.execute('ALTER TABLE dim_Facture ADD CONSTRAINT pk_Facture PRIMARY KEY (Facture_ID)')

cur.execute('CREATE TABLE dim_SRC (SRC_ID VARCHAR(20), SRC VARCHAR(20))')
cur.execute('ALTER TABLE dim_SRC ADD CONSTRAINT pk_SRC PRIMARY KEY (SRC_ID)')

cur.execute('CREATE TABLE dim_Engagement (Eng_ID VARCHAR(20), Type_Engagement VARCHAR(20))')
cur.execute('ALTER TABLE dim_Engagement ADD CONSTRAINT pk_Eng PRIMARY KEY (Eng_ID)')

# Create fact table with foreign key constraints
cur.execute('CREATE TABLE fact_Lig_CMD_Frn (Fournisseur_ID VARCHAR(150), DATE_Com_Frn_ID DATE, Commande_ID VARCHAR(150), Departement_ID VARCHAR(150), LIG_ID VARCHAR(20), Article_ID VARCHAR(150), Famille_ID VARCHAR(150), SFamille_ID VARCHAR(150), Titre_ID VARCHAR(150), ArticleBUD_ID VARCHAR(20), Paragraphe_ID VARCHAR(20), Qte_Art_Cd real, Pu_Art_Brut real, PU_ART_CD real, QTE_REST real, MNT_TTC real, MNT_HT real, MNT_REM real, MNT_TVA real, MNT_TAX real )')
cur.execute('ALTER TABLE fact_Lig_CMD_Frn ADD CONSTRAINT fk_Fournisseur FOREIGN KEY (Fournisseur_ID) REFERENCES dim_Fournisseur(Fournisseur_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Lig_CMD_Frn ADD CONSTRAINT fk_Com_Frn_date FOREIGN KEY (DATE_Com_Frn_ID) REFERENCES dim_date(DATE_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Lig_CMD_Frn ADD CONSTRAINT fk_Commande FOREIGN KEY (Commande_ID) REFERENCES dim_Commande(Commande_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Lig_CMD_Frn ADD CONSTRAINT fk_Departement FOREIGN KEY (Departement_ID) REFERENCES dim_Departement(Departement_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Lig_CMD_Frn ADD CONSTRAINT fk_LIG FOREIGN KEY (LIG_ID) REFERENCES dim_LIG(LIG_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Lig_CMD_Frn ADD CONSTRAINT fk_Article FOREIGN KEY (Article_ID) REFERENCES dim_Article(Article_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Lig_CMD_Frn ADD CONSTRAINT fk_Famille FOREIGN KEY (Famille_ID) REFERENCES dim_Famille(Famille_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Lig_CMD_Frn ADD CONSTRAINT fk_SFamille FOREIGN KEY (SFamille_ID) REFERENCES dim_SFamille(SFamille_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Lig_CMD_Frn ADD CONSTRAINT fk_Titre FOREIGN KEY (Titre_ID) REFERENCES dim_Titre(Titre_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Lig_CMD_Frn ADD CONSTRAINT fk_ArticleBUD FOREIGN KEY (ArticleBUD_ID) REFERENCES dim_ArticleBUD(ArticleBUD_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Lig_CMD_Frn ADD CONSTRAINT fk_Paragraphe FOREIGN KEY (Paragraphe_ID) REFERENCES dim_Paragraphe(Paragraphe_ID) ON DELETE CASCADE')

cur.execute('CREATE TABLE fact_Commande_Frn (Fournisseur_ID VARCHAR(150), DATE_Com_Frn_ID DATE, Commande_ID VARCHAR(150), Departement_ID VARCHAR(150), Type_CMD_ID VARCHAR(20), MT_TTC_ENG real, MT_HT_ENG real, MNT_TVA_ENG real , MNT_REM_ENG real, MNT_TAXE_ENG real)')
cur.execute('ALTER TABLE fact_Commande_Frn ADD CONSTRAINT fk_Fournisseur FOREIGN KEY (Fournisseur_ID) REFERENCES dim_Fournisseur(Fournisseur_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Commande_Frn ADD CONSTRAINT fk_Com_Frn_date FOREIGN KEY (DATE_Com_Frn_ID) REFERENCES dim_date(DATE_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Commande_Frn ADD CONSTRAINT fk_Commande FOREIGN KEY (Commande_ID) REFERENCES dim_Commande(Commande_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Commande_Frn ADD CONSTRAINT fk_Departement FOREIGN KEY (Departement_ID) REFERENCES dim_Departement(Departement_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Commande_Frn ADD CONSTRAINT fk_Type_CMD FOREIGN KEY (Type_CMD_ID) REFERENCES dim_Type_CMD(Type_CMD_ID) ON DELETE CASCADE')

cur.execute('CREATE TABLE fact_Lig_Fact_Frn (Fournisseur_ID VARCHAR(150), DATE_Fact_ID DATE, Facture_ID VARCHAR(150), LIG_ID VARCHAR(20), Article_ID VARCHAR(150), Famille_ID VARCHAR(150), SFamille_ID VARCHAR(150), Titre_ID VARCHAR(150), ArticleBUD_ID VARCHAR(150), Paragraphe_ID VARCHAR(150), Qtite_Art_Ligf real, Pu_Art_Ligf real, TAXE_ART_LIGF real, REM_ART_LIGF real, MNT_THT real, MNT_TVA real, MNT_REM real)')
cur.execute('ALTER TABLE fact_Lig_Fact_Frn ADD CONSTRAINT fk_Fournisseur FOREIGN KEY (Fournisseur_ID) REFERENCES dim_Fournisseur(Fournisseur_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Lig_Fact_Frn ADD CONSTRAINT fk_Fact_date FOREIGN KEY (DATE_Fact_ID) REFERENCES dim_date(DATE_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Lig_Fact_Frn ADD CONSTRAINT fk_Facture FOREIGN KEY (Facture_ID) REFERENCES dim_Facture(Facture_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Lig_Fact_Frn ADD CONSTRAINT fk_LIG FOREIGN KEY (LIG_ID) REFERENCES dim_LIG(LIG_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Lig_Fact_Frn ADD CONSTRAINT fk_Article FOREIGN KEY (Article_ID) REFERENCES dim_Article(Article_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Lig_Fact_Frn ADD CONSTRAINT fk_Famille FOREIGN KEY (Famille_ID) REFERENCES dim_Famille(Famille_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Lig_Fact_Frn ADD CONSTRAINT fk_SFamille FOREIGN KEY (SFamille_ID) REFERENCES dim_SFamille(SFamille_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Lig_Fact_Frn ADD CONSTRAINT fk_Titre FOREIGN KEY (Titre_ID) REFERENCES dim_Titre(Titre_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Lig_Fact_Frn ADD CONSTRAINT fk_ArticleBUD FOREIGN KEY (ArticleBUD_ID) REFERENCES dim_ArticleBUD(ArticleBUD_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Lig_Fact_Frn ADD CONSTRAINT fk_Paragraphe FOREIGN KEY (Paragraphe_ID) REFERENCES dim_Paragraphe(Paragraphe_ID) ON DELETE CASCADE')

cur.execute('CREATE TABLE fact_Facture_Frn (Fournisseur_ID VARCHAR(150), DATE_Com_Frn_ID DATE, DATE_Facture_ID DATE, Facture_ID VARCHAR(150), Departement_ID VARCHAR(150), Type_CMD_ID VARCHAR(20), Nat_Facture_ID VARCHAR(20), Com_Frn_ID VARCHAR(20), MNT_TTC_FAC real, MNT_HT_FAC real, MNT_TVA_FAC real, MNT_REM_FAC real, MNT_TAXE_FAC real)')
cur.execute('ALTER TABLE fact_Facture_Frn ADD CONSTRAINT fk_Fournisseur FOREIGN KEY (Fournisseur_ID) REFERENCES dim_Fournisseur(Fournisseur_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Facture_Frn ADD CONSTRAINT fk_Com_Frn_date FOREIGN KEY (DATE_Com_Frn_ID) REFERENCES dim_date(DATE_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Facture_Frn ADD CONSTRAINT fk_Facture_date FOREIGN KEY (DATE_Facture_ID) REFERENCES dim_date(DATE_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Facture_Frn ADD CONSTRAINT fk_Facture FOREIGN KEY (Facture_ID) REFERENCES dim_Facture(Facture_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Facture_Frn ADD CONSTRAINT fk_Departement FOREIGN KEY (Departement_ID) REFERENCES dim_Departement(Departement_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Facture_Frn ADD CONSTRAINT fk_Type_CMD FOREIGN KEY (Type_CMD_ID) REFERENCES dim_Type_CMD(Type_CMD_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_Facture_Frn ADD CONSTRAINT fk_Nat_Facture FOREIGN KEY (Nat_Facture_ID) REFERENCES dim_Nat_Facture(Nat_Facture_ID) ON DELETE CASCADE')

cur.execute('CREATE TABLE fact_V_detail_engagement (Fournisseur_ID VARCHAR(150), ANNEE_ID VARCHAR(4), DATE_Com_ID DATE, Commande_Eng_ID VARCHAR(150), Eng_ID VARCHAR(20), SRC_ID VARCHAR(20), Titre_ID VARCHAR(150), ArticleBUD_ID VARCHAR(150), Paragraphe_ID VARCHAR(150), MNT_DEV real, QTE_ENG real, Val_ENG real, QTE_FACT real, Val_FACT real, Val_REG real)')
cur.execute('ALTER TABLE fact_V_detail_engagement ADD CONSTRAINT fk_anneebud FOREIGN KEY (ANNEE_ID) REFERENCES dim_anneebud(ANNEE_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_V_detail_engagement ADD CONSTRAINT fk_Com_date FOREIGN KEY (DATE_COM_ID) REFERENCES dim_date(DATE_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_V_detail_engagement ADD CONSTRAINT fk_Fournisseur FOREIGN KEY (Fournisseur_ID) REFERENCES dim_Fournisseur(Fournisseur_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_V_detail_engagement ADD CONSTRAINT fk_Commande_Eng FOREIGN KEY (Commande_Eng_ID) REFERENCES dim_Commande_Eng(Commande_Eng_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_V_detail_engagement ADD CONSTRAINT fk_Titre FOREIGN KEY (Titre_ID) REFERENCES dim_Titre(Titre_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_V_detail_engagement ADD CONSTRAINT fk_ArticleBUD FOREIGN KEY (ArticleBUD_ID) REFERENCES dim_ArticleBUD(ArticleBUD_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_V_detail_engagement ADD CONSTRAINT fk_Paragraphe FOREIGN KEY (Paragraphe_ID) REFERENCES dim_Paragraphe(Paragraphe_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_V_detail_engagement ADD CONSTRAINT fk_SRC FOREIGN KEY (SRC_ID) REFERENCES dim_SRC(SRC_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_V_detail_engagement ADD CONSTRAINT fk_Eng FOREIGN KEY (Eng_ID) REFERENCES dim_Engagement(Eng_ID) ON DELETE CASCADE')

cur.execute('CREATE TABLE fact_suivi_engagement_bud (Annee_id VARCHAR(4), Titre_ID VARCHAR(150), ArticleBUD_ID VARCHAR(150), Paragraphe_ID VARCHAR(150), Prevision real, V_ENG real, V_FACT real, V_REG real)')
cur.execute('ALTER TABLE fact_suivi_engagement_bud ADD CONSTRAINT fk_anneebud FOREIGN KEY (ANNEE_ID) REFERENCES dim_anneebud(ANNEE_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_suivi_engagement_bud ADD CONSTRAINT fk_Titre FOREIGN KEY (Titre_ID) REFERENCES dim_Titre(Titre_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_suivi_engagement_bud ADD CONSTRAINT fk_ArticleBUD FOREIGN KEY (ArticleBUD_ID) REFERENCES dim_ArticleBUD(ArticleBUD_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_suivi_engagement_bud ADD CONSTRAINT fk_Paragraphe FOREIGN KEY (Paragraphe_ID) REFERENCES dim_Paragraphe(Paragraphe_ID) ON DELETE CASCADE')

con.commit()
