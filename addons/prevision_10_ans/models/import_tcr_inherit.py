from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
import base64
import datetime
from dateutil.relativedelta import relativedelta
from io import BytesIO
import xlsxwriter
import openpyxl

import numpy as np
import matplotlib.pyplot as plt

TCR_LIST = [
    ('1', "Chiffre d'affaire"),
    ('2', "Revente en l'état"),
    ('3', 'Production vendue'),
    ('4', 'Travaux'),
    ('5', 'Service'),
    ('6', 'Achats consommés'),
    ('7', "Autres charges externes"),
    ('8', "Valeur ajoutée d'exploitation"),
    ('9', 'Charges de personnel'),
    ('10', 'Impôts, taxes et versements assimilés'),
    ('11', "Excédent Brut d'Exploitation"),
    ('12', 'Autres produits opérationnels'),
    ('13', 'Autres charges opérationnelles'),
    ('14', 'Dotations aux amortissements'),
    ('15', 'Résultat Opérationnel'),
    ('16', 'Charges financières'),
    ('17', 'Résultat Ordinaire Avant Impôts'),
    ('18', "Impôts sur les bénéfices"),
    ('19', "Résultat Net"),
]
TCR_LIST_ar = [
    ('1', "Chiffre d'affaire", 'رقم الأعمال - المبيعات '),
    ('2', "Revente en l'état", 'إعادة البيع على الحالة'),
    ('3', 'Production vendue', 'الإنتاج المثبت '),
    ('4', 'Travaux', 'الاشغال'),
    ('5', 'Service', 'خدمات'),
    ('6', 'Achats consommés', 'مشتريات مستهلكة'),
    ('7', "Autres charges externes", 'خدمات خارجية ومشتريات أخرى'),
    ('8', "Valeur ajoutée d'exploitation", 'القيمة المضافة للاستغلال '),
    ('9', 'Charges de personnel', 'أعباء المستخدمين '),
    ('10', 'Impôts, taxes et versements assimilés', 'الضرائب والرسوم والمدفوعات المماثلة '),
    ('11', "Excédent Brut d'Exploitation", 'إجمالي فائض الاستغلال'),
    ('12', 'Autres produits opérationnels', 'المنتجات العملياتية الأخرى'),
    ('13', 'Autres charges opérationnelles', 'الأعباء العملياتية الأخرى'),
    ('14', 'Dotations aux amortissements', 'مخصصات الاستهلاك ،المؤونات وخسائر القيمة'),
    ('15', 'Résultat Opérationnel', 'النتيجة العملياتية'),
    ('16', 'Charges financières', 'الأعباء المالية'),
    ('17', 'Résultat Ordinaire Avant Impôts', 'النتيجة العادية قبل الضرائب'),
    ('18', "Impôts sur les bénéfices", 'الضرائب الواجب دفعها على النتائج العادية'),
    ('19', "Résultat Net", 'النتيجة الصافية للنشاطات العادية'),
]

Ratio_LIST = [
    ("1", "Marge brute"),
    ("2", "Marge brute %"),
    ("3", "EBE / CA %"),
    ("4", "RNC / CA %"),
    ("5", "CAF"),
    ("6", "CAF / CA %"),
    ("7", "FF / EBE %"),
]
Ratio_list_ar = [
    ('1', 'هامش الربح الإجمالي'),
    ('2', 'معدل هامش الربح %'),
    ('3', 'إجمالي فائض الاستغلال / رقم الأعمال %'),
    ('4', 'النتيجة الصافية / رقم الأعمال %'),
    ('5', 'القدرة على التمويل الذاتي'),
    ('6', 'قدرة التمويل الذاتي / رقم الأعمال %'),
    ('7', 'الأعباء المالية  / إجمالي فائض الاستغلال %'),
]

list_bilan = [
    ('1', 'تدفقات داخلة'),
    ('2', 'المبيعات'),
    ('3', 'تدفقات خارجة'),
    ('4', 'كلفة المبيعات'),
    ('5', 'المصاريف الإدارية والعمومية'),
    ('6', 'المصاريف التمويلية المرتبطة بالطلب'),
    ('7', 'Cash-flow  التدفقات النقدية'),
    ('8', 'صافي الربح'),
    ('9', 'الإهتلاكات و المؤونات'),
    ('10', 'CAF قدرة التمويل الذاتي'),
    ('11', 'الأقساط السنوية المرتبطة بالتمويلات الاستثمارية الحالية'),
    ('12', 'الأقساط السنوية المرتبطة بالطلب'),
    ('13', 'نسبة تغطية قدرة التمويل الذاتي للأقساط الإجمالية')
]

list_evaluation = [
    (1, 'المخزون'),
    (2, 'الزبائن'),
    (3, 'المـوردون'),
    (4, 'صافي راس المال العامل')
]

list_eval = [
    (1, 'إجمالي فائض الاستغلال'),
    (2, 'الضرائب الواجب دفعها على النتائج العادية'),
    (3, 'التغير في متطلبات رأس المال العامل'),
    (4, 'الأعباء المالية'),
    (5, 'التدفق النقدي الحر'),
]



class Cashflow(models.Model):
    _inherit = 'tcr.analysis.cashflow.line'
      
    amount_n6 = fields.Float(string='N+7 م/دج')
    amount_n6_dollar = fields.Float(string='م/$', compute='compute_dollar')

    amount_n7 = fields.Float(string='N+8 م/دج')
    amount_n7_dollar = fields.Float(string='م/$', compute='compute_dollar')

    amount_n8 = fields.Float(string='N+9 م/دج')
    amount_n8_dollar = fields.Float(string='م/$', compute='compute_dollar')

    amount_n9 = fields.Float(string='N+10 م/دج')
    amount_n9_dollar = fields.Float(string='م/$', compute='compute_dollar')

 

    def compute_dollar(self):
        for rec in self:
            rec.amount_n_dollar = rec.taux_change * rec.amount_n
            rec.amount_n1_dollar = rec.taux_change * rec.amount_n1
            rec.amount_n2_dollar = rec.taux_change * rec.amount_n2
            rec.amount_n3_dollar = rec.taux_change * rec.amount_n3
            rec.amount_n4_dollar = rec.taux_change * rec.amount_n4
            rec.amount_n5_dollar = rec.taux_change * rec.amount_n5
            rec.amount_n6_dollar = rec.taux_change * rec.amount_n6
            rec.amount_n7_dollar = rec.taux_change * rec.amount_n7
            rec.amount_n8_dollar = rec.taux_change * rec.amount_n8
            rec.amount_n9_dollar = rec.taux_change * rec.amount_n9
            
           
class Evaluation(models.Model):
    _inherit = 'tcr.analysis.evaluation.projet'


    
    amount_n6= fields.Float(string='N+6')
    amount_n7 = fields.Float(string='N+7')
    amount_n8 = fields.Float(string='N+8')
    amount_n9 = fields.Float(string='N+9')
    amount_n10 = fields.Float(string='N+10')
    


    def compute_montant(self):
        for rec in self:
            if rec.sequence == 4:
                bilan_1 = self.env['tcr.analysis.evaluation.projet'].search([('tcr_analysis_id', '=', rec.tcr_analysis_id.id),
                                                                             ('sequence', '=', 1)])
                bilan_2 = self.env['tcr.analysis.evaluation.projet'].search([('tcr_analysis_id', '=', rec.tcr_analysis_id.id),
                                                                             ('sequence', '=', 2)])
                bilan_3 = self.env['tcr.analysis.evaluation.projet'].search([('tcr_analysis_id', '=', rec.tcr_analysis_id.id),
                                                                             ('sequence', '=', 3)])
                rec.amount_n = bilan_1.amount_n + bilan_2.amount_n - bilan_3.amount_n
                rec.amount_n1 = bilan_1.amount_n1 + bilan_2.amount_n1 - bilan_3.amount_n1
                rec.amount_n2 = bilan_1.amount_n2 + bilan_2.amount_n2 - bilan_3.amount_n2
                rec.amount_n3 = bilan_1.amount_n3 + bilan_2.amount_n3 - bilan_3.amount_n3
                rec.amount_n4 = bilan_1.amount_n4 + bilan_2.amount_n4 - bilan_3.amount_n4
                rec.amount_n5 = bilan_1.amount_n5 + bilan_2.amount_n5 - bilan_3.amount_n5
                rec.amount_n6 = bilan_1.amount_n6 + bilan_2.amount_n6 - bilan_3.amount_n6
                rec.amount_n7 = bilan_1.amount_n7 + bilan_2.amount_n7 - bilan_3.amount_n7
                rec.amount_n8 = bilan_1.amount_n8 + bilan_2.amount_n8 - bilan_3.amount_n8
                rec.amount_n9 = bilan_1.amount_n9 + bilan_2.amount_n9 - bilan_3.amount_n9
                rec.amount_n10 = bilan_1.amount_n10 + bilan_2.amount_n10 - bilan_3.amount_n10
                
                
                rec.computed = True
            else:
                rec.computed = False


class Evaluation(models.Model):
    _inherit = 'tcr.analysis.evaluation.projet.line'


    amount_n6 = fields.Float(string='N+6')
    amount_n7 = fields.Float(string='N+7')
    amount_n8 = fields.Float(string='N+8')
    amount_n9 = fields.Float(string='N+9')
    amount_n10 = fields.Float(string='N+10')



class RatioTCRLinePrev(models.Model):
    _inherit = 'tcr.analysis.prev.ratio'



    amount_n6= fields.Float(string='N+7')
    amount_n7 = fields.Float(string='N+8')
    amount_n8 = fields.Float(string='N+9')
    amount_n9 = fields.Float(string='N+10')
    
   




    def compute_graph(self):
        for rec in self:
            data = [rec.amount_n, rec.amount_n1, rec.amount_n2, rec.amount_n3, rec.amount_n4, rec.amount_n5,rec.amount_n6,rec.amount_n7,rec.amount_n8,rec.amount_n9]

            fig, ax = plt.subplots(1, 1, figsize=(1.5, 0.25))
            ax.plot(data)
            for k, v in ax.spines.items():
                v.set_visible(False)
            ax.set_xticks([])
            ax.set_yticks([])

            plt.plot(len(data) - 1, data[len(data) - 1], )

            buf = BytesIO()
            plt.savefig(buf, format='jpeg', dpi=100)
            buf.seek(0)
            imageBase64 = base64.b64encode(buf.getvalue())
            buf.close()
            rec.graph = imageBase64              


class RatioTCRLine(models.Model):
    _inherit = 'tcr.analysis.ratio.line'



    amount_n5= fields.Float(string='N+6')
    amount_n6 = fields.Float(string='N+7')
    amount_n7 = fields.Float(string='N+8')
    amount_n8 = fields.Float(string='N+9')
    amount_n9 = fields.Float(string='N+10')


    def compute_graph(self):
        for rec in self:
            data = [rec.amount_n3, rec.amount_n2, rec.amount_n1, rec.amount_n,rec.amount_n5,rec.amount_n6,rec.amount_n7,rec.amount_n8,rec.amount_n9]

            fig, ax = plt.subplots(1, 1, figsize=(1.5, 0.25))
            ax.plot(data)
            for k, v in ax.spines.items():
                v.set_visible(False)
            ax.set_xticks([])
            ax.set_yticks([])

            plt.plot(len(data) - 1, data[len(data) - 1], )

            buf = BytesIO()
            plt.savefig(buf, format='jpeg', dpi=100)
            buf.seek(0)
            imageBase64 = base64.b64encode(buf.getvalue())
            buf.close()
            rec.graph = imageBase64


class TCRprev(models.Model):
    _inherit = 'tcr.analysis.prev'





    amount_n6 = fields.Float(string="N+6")
    amount_n7 = fields.Float(string="N+7")
    amount_n8 = fields.Float(string="N+8")
    amount_n9 = fields.Float(string="N+9")
  


    augment_hypothesis_n6 = fields.Float(string="Hypothèse croissance N+6", digits=(16, 2))
    augment_hypothesis_n7 = fields.Float(string="Hypothèse croissance N+7", digits=(16, 2))
    augment_hypothesis_n8 = fields.Float(string="Hypothèse croissance N+8", digits=(16, 2))
    augment_hypothesis_n9 = fields.Float(string="Hypothèse croissance N+9", digits=(16, 2))
    augment_hypothesis_n10 = fields.Float(string="Hypothèse croissance N+10", digits=(16, 2))



class ImportTCRLine(models.Model):
    _inherit = 'tcr.analysis.import.line'



    amount_n5= fields.Float(string='N+6')
    amount_n6 = fields.Float(string='N+7')
    amount_n7 = fields.Float(string='N+8')
    amount_n8 = fields.Float(string='N+9')
    amount_n9 = fields.Float(string='N+10')
           
           
           
           
           
           
           
           
           
           
           
           
           
    
    
    
    
    
class TCRAnalysis(models.Model):
    _inherit = 'tcr.analysis.import'

    
    
    def calcul_cashflow(self):
        
        for rec in self:
            bilan_1 = rec.cashflow_ids.filtered(lambda l: l.bilan == 1)
            bilan_2 = rec.cashflow_ids.filtered(lambda l: l.bilan == 2)
            recap_1 = rec.recap_tcr_prev_ids.filtered(lambda l: l.poste_comptable == '1')
            bilan_1.amount_n = bilan_2.amount_n = recap_1.amount_n
            bilan_1.amount_n1 = bilan_2.amount_n1 = recap_1.amount_n1
            bilan_1.amount_n2 = bilan_2.amount_n2 = recap_1.amount_n2
            bilan_1.amount_n3 = bilan_2.amount_n3 = recap_1.amount_n3
            bilan_1.amount_n4 = bilan_2.amount_n4 = recap_1.amount_n4
            bilan_1.amount_n5 = bilan_2.amount_n5 = recap_1.amount_n5
            bilan_1.amount_n6 = bilan_2.amount_n6 = recap_1.amount_n6
            bilan_1.amount_n7 = bilan_2.amount_n7 = recap_1.amount_n7
            bilan_1.amount_n8 = bilan_2.amount_n8 = recap_1.amount_n8
            bilan_1.amount_n9 = bilan_2.amount_n9 = recap_1.amount_n9
            

            bilan_3 = rec.cashflow_ids.filtered(lambda l: l.bilan == 3)
            bilan_4 = rec.cashflow_ids.filtered(lambda l: l.bilan == 4)
            bilan_5 = rec.cashflow_ids.filtered(lambda l: l.bilan == 5)
            bilan_6 = rec.cashflow_ids.filtered(lambda l: l.bilan == 6)
            bilan_15 = rec.cashflow_ids.filtered(lambda l: l.bilan == 12)
            recap_2 = rec.recap_tcr_prev_ids.filtered(lambda l: l.poste_comptable == '6')
            bilan_4.amount_n = recap_2.amount_n
            bilan_4.amount_n1 = recap_2.amount_n1
            bilan_4.amount_n2 = recap_2.amount_n2
            bilan_4.amount_n3 = recap_2.amount_n3
            bilan_4.amount_n4 = recap_2.amount_n4
            bilan_4.amount_n5 = recap_2.amount_n5
            bilan_4.amount_n6 = recap_2.amount_n6
            bilan_4.amount_n7 = recap_2.amount_n7
            bilan_4.amount_n8 = recap_2.amount_n8
            bilan_4.amount_n9 = recap_2.amount_n9
           

            recap_3 = rec.recap_tcr_prev_ids.filtered(lambda l: l.poste_comptable == '7')
            bilan_5.amount_n = recap_3.amount_n
            bilan_5.amount_n1 = recap_3.amount_n1
            bilan_5.amount_n2 = recap_3.amount_n2
            bilan_5.amount_n3 = recap_3.amount_n3
            bilan_5.amount_n4 = recap_3.amount_n4
            bilan_5.amount_n5 = recap_3.amount_n5
            bilan_5.amount_n6 = recap_3.amount_n6
            bilan_5.amount_n7 = recap_3.amount_n7
            bilan_5.amount_n8 = recap_3.amount_n8
            bilan_5.amount_n9 = recap_3.amount_n9
           

            somme = somme_annee = count = 0
            year = rec.echeance_ids[0].date.year if rec.echeance_ids else 0
            if year != 0:
                for item in rec.echeance_ids:
                    if year == item.date.year:
                        somme += item.marge
                        somme_annee += item.principal
                    else:
                        if count == 0:
                            bilan_6.amount_n = somme
                            bilan_15.amount_n = somme_annee
                        elif count == 1:
                            bilan_6.amount_n1 = somme
                            bilan_15.amount_n1 = somme_annee
                        elif count == 2:
                            bilan_6.amount_n2 = somme
                            bilan_15.amount_n2 = somme_annee
                        elif count == 3:
                            bilan_6.amount_n3 = somme
                            bilan_15.amount_n3 = somme_annee
                        elif count == 4:
                            bilan_6.amount_n4 = somme
                            bilan_15.amount_n4 = somme_annee
                        elif count == 5:
                            bilan_6.amount_n5 = somme
                            bilan_15.amount_n5 = somme_annee
                        elif count == 6:
                            bilan_6.amount_n6 = somme
                            bilan_15.amount_n6 = somme_annee
                        elif count == 7:
                            bilan_6.amount_n7 = somme
                            bilan_15.amount_n7 = somme_annee
                        elif count == 8:
                            bilan_6.amount_n8 = somme
                            bilan_15.amount_n8 = somme_annee
                        elif count == 9:
                            bilan_6.amount_n9 = somme
                            bilan_15.amount_n9 = somme_annee
                        somme = item.marge
                        somme_annee = item.total
                        count += 1
                    year = item.date.year

                if count == 0:
                    bilan_6.amount_n = somme
                    bilan_15.amount_n = somme_annee
                elif count == 1:
                    bilan_6.amount_n1 = somme
                    bilan_15.amount_n1 = somme_annee
                elif count == 2:
                    bilan_6.amount_n2 = somme
                    bilan_15.amount_n2 = somme_annee
                elif count == 3:
                    bilan_6.amount_n3 = somme
                    bilan_15.amount_n3 = somme_annee
                elif count == 4:
                    bilan_6.amount_n4 = somme
                    bilan_15.amount_n4 = somme_annee
                elif count == 5:
                    bilan_6.amount_n5 = somme
                    bilan_15.amount_n5 = somme_annee
                elif count == 6:
                    bilan_6.amount_n6 = somme
                    bilan_15.amount_n6 = somme_annee
                elif count == 7:
                    bilan_6.amount_n7 = somme
                    bilan_15.amount_n7 = somme_annee
                elif count == 8:
                    bilan_6.amount_n8 = somme
                    bilan_15.amount_n8 = somme_annee
                elif count == 9:
                    bilan_6.amount_n9 = somme
                    bilan_15.amount_n9 = somme_annee
                elif count == 10:
                    bilan_6.amount_n10 = somme
                    bilan_15.amount_n10 = somme_annee
            bilan_3.amount_n = bilan_4.amount_n + bilan_5.amount_n + bilan_6.amount_n
            bilan_3.amount_n1 = bilan_4.amount_n1 + bilan_5.amount_n1 + bilan_6.amount_n1
            bilan_3.amount_n2 = bilan_4.amount_n2 + bilan_5.amount_n2 + bilan_6.amount_n2
            bilan_3.amount_n3 = bilan_4.amount_n3 + bilan_5.amount_n3 + bilan_6.amount_n3
            bilan_3.amount_n4 = bilan_4.amount_n4 + bilan_5.amount_n4 + bilan_6.amount_n4
            bilan_3.amount_n5 = bilan_4.amount_n5 + bilan_5.amount_n5 + bilan_6.amount_n5
            bilan_3.amount_n6 = bilan_4.amount_n6 + bilan_5.amount_n6 + bilan_6.amount_n6
            bilan_3.amount_n7 = bilan_4.amount_n7 + bilan_5.amount_n7 + bilan_6.amount_n7
            bilan_3.amount_n8 = bilan_4.amount_n8 + bilan_5.amount_n8 + bilan_6.amount_n8
            bilan_3.amount_n9 = bilan_4.amount_n9 + bilan_5.amount_n9 + bilan_6.amount_n9
            
            bilan_7 = rec.cashflow_ids.filtered(lambda l: l.bilan == 7)
            bilan_8 = rec.cashflow_ids.filtered(lambda l: l.bilan == 8)
            bilan_9 = rec.cashflow_ids.filtered(lambda l: l.bilan == 9)
            bilan_10 = rec.cashflow_ids.filtered(lambda l: l.bilan == 10)
            bilan_11 = rec.cashflow_ids.filtered(lambda l: l.bilan == 11)
            bilan_13 = rec.cashflow_ids.filtered(lambda l: l.bilan == 13)
            bilan_7.amount_n = bilan_1.amount_n - bilan_3.amount_n
            bilan_7.amount_n1 = bilan_1.amount_n1 - bilan_3.amount_n1
            bilan_7.amount_n2 = bilan_1.amount_n2 - bilan_3.amount_n2
            bilan_7.amount_n3 = bilan_1.amount_n3 - bilan_3.amount_n3
            bilan_7.amount_n4 = bilan_1.amount_n4 - bilan_3.amount_n4
            bilan_7.amount_n5 = bilan_1.amount_n5 - bilan_3.amount_n5
            bilan_7.amount_n6 = bilan_1.amount_n6 - bilan_3.amount_n6
            bilan_7.amount_n7 = bilan_1.amount_n7 - bilan_3.amount_n7
            bilan_7.amount_n8 = bilan_1.amount_n8 - bilan_3.amount_n8
            bilan_7.amount_n9 = bilan_1.amount_n9 - bilan_3.amount_n9
            
            recap_4 = rec.recap_tcr_prev_ids.filtered(lambda l: l.poste_comptable == '19')
            bilan_8.amount_n = recap_4.amount_n
            bilan_8.amount_n1 = recap_4.amount_n1
            bilan_8.amount_n2 = recap_4.amount_n2
            bilan_8.amount_n3 = recap_4.amount_n3
            bilan_8.amount_n4 = recap_4.amount_n4
            bilan_8.amount_n5 = recap_4.amount_n5
            bilan_8.amount_n6 = recap_4.amount_n6
            bilan_8.amount_n7 = recap_4.amount_n7
            bilan_8.amount_n8 = recap_4.amount_n8
            bilan_8.amount_n9 = recap_4.amount_n9
            recap_5 = rec.recap_tcr_prev_ids.filtered(lambda l: l.poste_comptable == '14')
            bilan_9.amount_n = recap_5.amount_n
            bilan_9.amount_n1 = recap_5.amount_n1
            bilan_9.amount_n2 = recap_5.amount_n2
            bilan_9.amount_n3 = recap_5.amount_n3
            bilan_9.amount_n4 = recap_5.amount_n4
            bilan_9.amount_n5 = recap_5.amount_n5
            bilan_9.amount_n6 = recap_5.amount_n6
            bilan_9.amount_n7 = recap_5.amount_n7
            bilan_9.amount_n8 = recap_5.amount_n8
            bilan_9.amount_n9 = recap_5.amount_n9
            
            recap_6 = rec.tcr_prev_ratio_ids.filtered(lambda l: l.ratio == '5')
            bilan_10.amount_n = recap_6.amount_n
            bilan_10.amount_n1 = recap_6.amount_n1
            bilan_10.amount_n2 = recap_6.amount_n2
            bilan_10.amount_n3 = recap_6.amount_n3
            bilan_10.amount_n4 = recap_6.amount_n4
            bilan_10.amount_n5 = recap_6.amount_n5
            bilan_10.amount_n6 = recap_6.amount_n6
            bilan_10.amount_n7 = recap_6.amount_n7
            bilan_10.amount_n8 = recap_6.amount_n8
            bilan_10.amount_n9 = recap_6.amount_n9
            bilan_13.amount_n = (bilan_10.amount_n / (bilan_11.amount_n + bilan_15.amount_n)) if bilan_11.amount_n + bilan_15.amount_n != 0 else 0
            bilan_13.amount_n1 = (bilan_10.amount_n1 / (bilan_11.amount_n1 + bilan_15.amount_n1)) if bilan_11.amount_n1 + bilan_15.amount_n1 != 0 else 0
            bilan_13.amount_n2 = (bilan_10.amount_n2 / (bilan_11.amount_n2 + bilan_15.amount_n2)) if bilan_11.amount_n2 + bilan_15.amount_n2 != 0 else 0
            bilan_13.amount_n3 = (bilan_10.amount_n3 / (bilan_11.amount_n3 + bilan_15.amount_n3)) if bilan_11.amount_n3 + bilan_15.amount_n3 != 0 else 0
            bilan_13.amount_n4 = (bilan_10.amount_n4 / (bilan_11.amount_n4 + bilan_15.amount_n4)) if bilan_11.amount_n4 + bilan_15.amount_n4 != 0 else 0
            bilan_13.amount_n5 = (bilan_10.amount_n5 / (bilan_11.amount_n5 + bilan_15.amount_n5)) if bilan_11.amount_n5 + bilan_15.amount_n5 != 0 else 0
            bilan_13.amount_n6 = (bilan_10.amount_n6 / (bilan_11.amount_n6 + bilan_15.amount_n6)) if bilan_11.amount_n6 + bilan_15.amount_n6 != 0 else 0
            bilan_13.amount_n7 = (bilan_10.amount_n7 / (bilan_11.amount_n7 + bilan_15.amount_n7)) if bilan_11.amount_n7 + bilan_15.amount_n7 != 0 else 0
            bilan_13.amount_n8 = (bilan_10.amount_n8 / (bilan_11.amount_n8 + bilan_15.amount_n8)) if bilan_11.amount_n8 + bilan_15.amount_n8 != 0 else 0
            bilan_13.amount_n9 = (bilan_10.amount_n9 / (bilan_11.amount_n9 + bilan_15.amount_n9)) if bilan_11.amount_n9 + bilan_15.amount_n9 != 0 else 0
           

    def calcul_evaluation(self):
        for rec in self:
            bilan_1 = rec.evaluation_line_ids.filtered(lambda l: l.sequence == 1)
            recap_1 = rec.recap_tcr_prev_ids.filtered(lambda l: l.poste_comptable == '11')
            bilan_1.amount_n1 = recap_1.amount_n
            bilan_1.amount_n2 = recap_1.amount_n1
            bilan_1.amount_n3 = recap_1.amount_n2
            bilan_1.amount_n4 = recap_1.amount_n3
            bilan_1.amount_n5 = recap_1.amount_n4
            bilan_1.amount_n6 = recap_1.amount_n5
            bilan_1.amount_n7 = recap_1.amount_n6
            bilan_1.amount_n8 = recap_1.amount_n7
            bilan_1.amount_n9 = recap_1.amount_n8
            bilan_1.amount_n10 = recap_1.amount_n9

            bilan_2 = rec.evaluation_line_ids.filtered(lambda l: l.sequence == 2)
            cash_2 = rec.cashflow_ids.filtered(lambda l: l.bilan == 6)
            recap_2 = rec.recap_tcr_prev_ids.filtered(lambda l: l.poste_comptable == '18')
            bilan_2.amount_n1 = recap_2.amount_n
            bilan_2.amount_n2 = recap_2.amount_n1
            bilan_2.amount_n3 = recap_2.amount_n2
            bilan_2.amount_n4 = recap_2.amount_n3
            bilan_2.amount_n5 = recap_2.amount_n4
            bilan_2.amount_n6 = recap_2.amount_n5
            bilan_2.amount_n7 = recap_2.amount_n6
            bilan_2.amount_n8 = recap_2.amount_n7
            bilan_2.amount_n9 = recap_2.amount_n8
            bilan_2.amount_n10 = recap_2.amount_n9


            bilan_3 = rec.evaluation_line_ids.filtered(lambda l: l.sequence == 3)
            bilan_init_1 = rec.evaluation_ids.filtered(lambda l: l.sequence == 4)

            bilan_3.amount_n1 = bilan_init_1.amount_n - bilan_init_1.amount_n1
            bilan_3.amount_n2 = bilan_init_1.amount_n1 - bilan_init_1.amount_n2
            bilan_3.amount_n3 = bilan_init_1.amount_n2 - bilan_init_1.amount_n3
            bilan_3.amount_n4 = bilan_init_1.amount_n3 - bilan_init_1.amount_n4
            bilan_3.amount_n5 = bilan_init_1.amount_n4 - bilan_init_1.amount_n5
            bilan_3.amount_n6 = bilan_init_1.amount_n5 - bilan_init_1.amount_n6
            bilan_3.amount_n7 = bilan_init_1.amount_n6 - bilan_init_1.amount_n7
            bilan_3.amount_n8 = bilan_init_1.amount_n7 - bilan_init_1.amount_n8
            bilan_3.amount_n9 = bilan_init_1.amount_n8 - bilan_init_1.amount_n9
            bilan_3.amount_n10 = bilan_init_1.amount_n9 - bilan_init_1.amount_n10


            bilan_4 = rec.evaluation_line_ids.filtered(lambda l: l.sequence == 4)
            recap_3 = rec.recap_tcr_prev_ids.filtered(lambda l: l.poste_comptable == '16')

            bilan_4.amount_n1 = recap_3.amount_n + cash_2.amount_n
            bilan_4.amount_n2 = recap_3.amount_n1 + cash_2.amount_n1
            bilan_4.amount_n3 = recap_3.amount_n2 + cash_2.amount_n2
            bilan_4.amount_n4 = recap_3.amount_n3 + cash_2.amount_n3
            bilan_4.amount_n5 = recap_3.amount_n4 + cash_2.amount_n4
            bilan_4.amount_n6 = recap_3.amount_n5 + cash_2.amount_n5
            bilan_4.amount_n7 = recap_3.amount_n6 + cash_2.amount_n6
            bilan_4.amount_n8 = recap_3.amount_n7 + cash_2.amount_n7
            bilan_4.amount_n9 = recap_3.amount_n8 + cash_2.amount_n8
            bilan_4.amount_n10 = recap_3.amount_n9 + cash_2.amount_n9


            bilan_5 = rec.evaluation_line_ids.filtered(lambda l: l.sequence == 5)

            bilan_5.amount_n1 = bilan_1.amount_n1 - bilan_2.amount_n1 + bilan_3.amount_n1 - bilan_4.amount_n1
            bilan_5.amount_n2 = bilan_1.amount_n2 - bilan_2.amount_n2 + bilan_3.amount_n2 - bilan_4.amount_n2
            bilan_5.amount_n3 = bilan_1.amount_n3 - bilan_2.amount_n3 + bilan_3.amount_n3 - bilan_4.amount_n3
            bilan_5.amount_n4 = bilan_1.amount_n4 - bilan_2.amount_n4 + bilan_3.amount_n4 - bilan_4.amount_n4
            bilan_5.amount_n5 = bilan_1.amount_n5 - bilan_2.amount_n5 + bilan_3.amount_n5 - bilan_4.amount_n5
            bilan_5.amount_n6 = bilan_1.amount_n6 - bilan_2.amount_n6 + bilan_3.amount_n6 - bilan_4.amount_n6
            bilan_5.amount_n7 = bilan_1.amount_n7 - bilan_2.amount_n7 + bilan_3.amount_n7 - bilan_4.amount_n7
            bilan_5.amount_n8 = bilan_1.amount_n8 - bilan_2.amount_n8 + bilan_3.amount_n8 - bilan_4.amount_n8
            bilan_5.amount_n9 = bilan_1.amount_n9 - bilan_2.amount_n9 + bilan_3.amount_n9 - bilan_4.amount_n9
            bilan_5.amount_n10 = bilan_1.amount_n10 - bilan_2.amount_n10 + bilan_3.amount_n10 - bilan_4.amount_n10

            cashflows = [bilan_5.amount_n1, bilan_5.amount_n2, bilan_5.amount_n3, bilan_5.amount_n4, bilan_5.amount_n5]
            van = calculate_npv(cashflows, rec.taux_rend)
            rec.van = van
    
           
        
    def action_validate(self):
        self.ensure_one()
        self.file_tester = True
        self.tcr_prev_ids.unlink()
        for rec in self.line_ids:
            self.env['tcr.analysis.prev'].create({
                'tcr_analysis_id': self.id,
                'amount_n': rec.amount_n,
                'amount_n1': rec.amount_n1,
                'amount_n2': rec.amount_n2,
                'amount_n3': rec.amount_n3,
                'amount_n4': rec.amount_n4,
                'amount_n5': rec.amount_n5,
                'amount_n6': rec.amount_n6,
                'amount_n7': rec.amount_n7,
                'amount_n8': rec.amount_n8,
                'amount_n9': rec.amount_n9,
                'poste_comptable': rec.poste_comptable,
                'poste_arabe': rec.poste_arabe
            })

        print(get_data(self.line_ids, type_class=2))
        self.graph_historical_bar = create_bar2(get_data(self.line_ids, type_class=2), type_class=2)
        self.graph_historical_bar_emp = create_bar(get_data(self.line_ids, type_class=2), type_class=2)
           
           
           
           
    def action_import_data(self):
        self.ensure_one()
        wb = openpyxl.load_workbook(filename=BytesIO(base64.b64decode(self.file_import_data)), read_only=True)
        ws = wb.active
        search = self.env['tcr.analysis.import.line'].search([('tcr_analysis_id', '=', self.id)]).unlink()
        count = 0
        for record in ws.iter_rows(min_row=2, max_row=None, min_col=None, max_col=None, values_only=True):
            count += 1
            if count <= 19:
                print(count)
                print(TCR_LIST[count - 1])
                print(record)
                try:
                    self.env['tcr.analysis.import.line'].create({
                        'tcr_analysis_id': self.id,
                        'poste_comptable': TCR_LIST[count-1][0],
                        'poste_arabe': TCR_LIST_ar[count-1][2],
                        'amount_n9': record[10],
                        'amount_n8': record[9],
                        'amount_n7': record[8],
                        'amount_n6': record[7],
                        'amount_n5': record[6],
                        'amount_n4': record[5],
                        'amount_n3': record[4],
                        'amount_n2': record[3],
                        'amount_n1': record[2],
                        'amount_n': record[1],
                    })
                except:
                    self.env['tcr.analysis.import.line'].create({
                        'tcr_analysis_id': self.id,
                        'poste_comptable': TCR_LIST[count-1][0],
                        'poste_arabe': TCR_LIST_ar[count-1][2],
                        'amount_n9': 0,
                        'amount_n8': 0,
                        'amount_n7': 0,
                        'amount_n6': 0,
                        'amount_n5': 0,
                        'amount_n4': 0,
                        'amount_n3': 0,
                        'amount_n2': 0,
                        'amount_n1': 0,
                        'amount_n': 0,
                    })
        calculFormule(self.line_ids)

    def action_count_ratio_hist(self):
        self.ensure_one()
        self.ratio_ids.unlink()
        if self.line_ids:
            for index, entry in Ratio_LIST:
                list_amounts = get_amount(self.line_ids, self.ratio_ids, index)
                ratio = self.env['tcr.analysis.ratio.line'].create({
                    'tcr_analysis_id': self.id,
                    'ratio': index,
                    'amount_n': list_amounts[0],
                    'amount_n1': list_amounts[1],
                    'amount_n2': list_amounts[2],
                    'amount_n3': list_amounts[3],
                    'amount_n4': list_amounts[4],
                    'amount_n5': list_amounts[5],
                    'amount_n6': list_amounts[6],
                    'amount_n7': list_amounts[7],
                    'amount_n8': list_amounts[8],
                    'amount_n9': list_amounts[9]})

    def action_count_prev(self):
        self.ensure_one()
        if self.tcr_prev_ids:
            for rec in self.tcr_prev_ids:
                if rec.poste_comptable not in ('1', '8', '11', '15', '17', '19'):
                    line = self.line_ids.filtered(lambda l: l.poste_comptable == rec.poste_comptable)
                    if line:  # Check if a matching line was found!
                        rec.amount_n = line.amount_n or 0.0  # Handle potential missing values
                        rec.amount_n1 = line.amount_n1 or 0.0
                        rec.amount_n2 = line.amount_n2 or 0.0
                        rec.amount_n3 = line.amount_n3 or 0.0
                        rec.amount_n4 = line.amount_n4 or 0.0
                        rec.amount_n5 = line.amount_n5 or 0.0
                        rec.amount_n6 = line.amount_n6 or 0.0
                        rec.amount_n7 = line.amount_n7 or 0.0
                        rec.amount_n8 = line.amount_n8 or 0.0
                        rec.amount_n9 = line.amount_n9 or 0.0

                        # Get augment_hypothesis values as floats, handling recordsets and missing values:
                        augment_n1 = rec.augment_hypothesis_n1 and float(rec.augment_hypothesis_n1) or 0.0
                        augment_n2 = rec.augment_hypothesis_n2 and float(rec.augment_hypothesis_n2) or 0.0
                        augment_n3 = rec.augment_hypothesis_n3 and float(rec.augment_hypothesis_n3) or 0.0
                        augment_n4 = rec.augment_hypothesis_n4 and float(rec.augment_hypothesis_n4) or 0.0
                        augment_n5 = rec.augment_hypothesis_n5 and float(rec.augment_hypothesis_n5) or 0.0
                        augment_n6 = rec.augment_hypothesis_n6 and float(rec.augment_hypothesis_n6) or 0.0
                        augment_n7 = rec.augment_hypothesis_n7 and float(rec.augment_hypothesis_n7) or 0.0
                        augment_n8 = rec.augment_hypothesis_n8 and float(rec.augment_hypothesis_n8) or 0.0
                        augment_n9 = rec.augment_hypothesis_n9 and float(rec.augment_hypothesis_n9) or 0.0
                        augment_n10 = rec.augment_hypothesis_n10 and float(rec.augment_hypothesis_n10) or 0.0

                        rec.amount_n = rec.amount_n * (augment_n1 / 100 + 1)
                        rec.amount_n1 = rec.amount_n1 * (augment_n2 / 100 + 1)
                        rec.amount_n2 = rec.amount_n2 * (augment_n3 / 100 + 1)
                        rec.amount_n3 = rec.amount_n3 * (augment_n4 / 100 + 1)
                        rec.amount_n4 = rec.amount_n4 * (augment_n5 / 100 + 1)
                        rec.amount_n5 = rec.amount_n5 * (augment_n5 / 100 + 1)
                        rec.amount_n6 = rec.amount_n6 * (augment_n6 / 100 + 1)
                        rec.amount_n7 = rec.amount_n7 * (augment_n7 / 100 + 1)
                        rec.amount_n8 = rec.amount_n8 * (augment_n8 / 100 + 1)
                        rec.amount_n9 = rec.amount_n9 * (augment_n9 / 100 + 1)
                        

                    else:
                        # Handle the case where no matching line is found.  This is CRUCIAL!
                        
                        rec.amount_n = 0.0
                        rec.amount_n1 = 0.0
                        rec.amount_n2 = 0.0
                        rec.amount_n3 = 0.0
                        rec.amount_n4 = 0.0
                        rec.amount_n5 = 0.0
                        rec.amount_n6 = 0.0
                        rec.amount_n7 = 0.0
                        rec.amount_n8 = 0.0
                        rec.amount_n9 = 0.0
                        
                    
            calculFormule(self.tcr_prev_ids)
            self.tcr_prev_ratio_ids.unlink()
            for index, entry in Ratio_LIST:
                list_amounts = get_amount(self.tcr_prev_ids, self.tcr_prev_ratio_ids, index, is_prev=1)
                ratio = self.env['tcr.analysis.prev.ratio'].create({
                    'tcr_analysis_id': self.id,
                    'ratio': index,
                    'amount_n': list_amounts[0],
                    'amount_n1': list_amounts[1],
                    'amount_n2': list_amounts[2],
                    'amount_n3': list_amounts[3],
                    'amount_n4': list_amounts[4],
                    'amount_n5': list_amounts[5],
                    'amount_n6': list_amounts[6],
                    'amount_n7': list_amounts[7],
                    'amount_n8': list_amounts[8],
                    'amount_n9': list_amounts[9],})  
            self.recap_tcr_prev_ids = self.tcr_prev_ids
            self.graph_prev_bar = create_stacked_chart(get_data(self.tcr_prev_ids,type_class=2))
            self.graph_prev_bar_emp = create_bar(get_data(self.tcr_prev_ids,type_class=2))
            self.cashflow_ids.unlink()
            for index, entry in list_bilan:
                print(type(index))
                print(entry)
                bilan = self.env['tcr.analysis.cashflow.line'].create({
                    'tcr_analysis_id': self.id,
                    'taux_change': self.taux_change,
                    'bilan': int(index),
                    'name': entry,
                    'amount_n': 0,
                    'amount_n1': 0,
                    'amount_n2': 0,
                    'amount_n3': 0,
                    'amount_n4': 0,
                    'amount_n5': 0,
                    'amount_n6': 0,
                    'amount_n7': 0,
                    'amount_n8': 0,
                    'amount_n9': 0,
                    })     
            self.evaluation_ids.unlink()
            for index, entry in list_evaluation:
                bilan = self.env['tcr.analysis.evaluation.projet'].create({
                    'tcr_analysis_id': self.id,
                    'sequence': int(index),
                    'name': entry,
                    'amount_n': 0,
                    'amount_n1': 0,
                    'amount_n2': 0,
                    'amount_n3': 0,
                    'amount_n4': 0,
                    'amount_n5': 0,
                    'amount_n6': 0,
                    'amount_n7': 0,
                    'amount_n8': 0,
                    'amount_n9': 0,})   
            self.evaluation_line_ids.unlink()
            for index, entry in list_eval:
                bilan = self.env['tcr.analysis.evaluation.projet.line'].create({
                    'tcr_analysis_id': self.id,
                    'sequence': int(index),
                    'name': entry,
                    'amount_n1': 0,
                    'amount_n2': 0,
                    'amount_n3': 0,
                    'amount_n4': 0,
                    'amount_n5': 0,
                    'amount_n6': 0,
                    'amount_n7': 0,
                    'amount_n8': 0,
                    'amount_n9': 0,
                    })       
        else:
            raise ValidationError("Vous devriez d'abord valider les données")

    @api.onchange('year_prec')
    def compute_graph_prec(self):
        if self.year_prec:
            records_ca = self.line_ids.filtered(lambda r: r.poste_comptable in ['2', '3', '4', '5'])
            labels = []
            sizes = []
            data = get_data(records_ca, type_class=2)
            for lab in data:
                if list(lab.values())[int(self.year_prec) + 1] != 0:
                    labels.append(list(lab.values())[0])
                    sizes.append(list(lab.values())[int(self.year_prec) + 1])

            img = create_pie(sizes, labels=labels)
            self.write({'graph_historical_pie_ca_by_exercise': img})

    @api.depends('year_suiv')
    def compute_graph_suiv(self):
        if self.year_suiv and self.recap_tcr_prev_ids:
            records_ca = self.recap_tcr_prev_ids.filtered(lambda r: r.poste_comptable in ['2', '3', '4', '5'])
            labels = []
            sizes = []
            data = get_data(records_ca, )
            print(len(data))
            for lab in data:
                print(int(self.year_suiv) + 1)
                print(len(list(lab.values())))
                if list(lab.values())[int(self.year_suiv) + 1] != 0:
                    labels.append(list(lab.values())[0])
                    sizes.append(list(lab.values())[int(self.year_suiv) + 1])
            print(labels)
            print(sizes)
            img = create_pie(sizes, labels=labels)
            self.write({'graph_prev_pie_ca_by_exercise': img})
        else:
            self.graph_prev_pie_by_exercise = None
            self.graph_prev_pie_ca_by_exercise = None











def get_value(value):
    data_get = ''
    for index, entry in TCR_LIST:
        if entry == value:
            data_get = index
    return data_get


def calculate_npv(cashflows, discount_rate):
    npv = 0.0
    for t, cf in enumerate(cashflows):
        print(t)
        print(cf)
        print(discount_rate)
        npv += cf / ((1 + discount_rate) ** (t + 1))
    return npv

def create_stacked_chart(data, type_class=1):
    data_tmp_1 = list(data[0].values())[1:]
    data_tmp_2 = list(data[10].values())[1:]
    data_tmp_3 = list(data[18].values())[1:]
    data1 = data_tmp_1
    data2 = data_tmp_2
    data3 = data_tmp_3
    year = ["N+1", "N+2", "N+3", "N+4", "N+5","N+6", "N+7", "N+8", "N+9", "N+10"]
    x = np.arange(len(year))  # the label locations
    width = 0.25  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x, data1, width, color="blue", label="Chiffre d'affaire")
    rects2 = ax.bar(x + width, data2, width, color="orange", label="EBE")
    rects3 = ax.bar(x + width * 2, data3, width, color="grey", label="Résultat Net")

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Montant')
    ax.set_title('Montant par année')
    ax.set_xticks(x + width, year)
    ax.legend(loc="lower left", bbox_to_anchor=(0.8, 1.0))

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    ax.bar_label(rects3, padding=3)

    fig.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='jpeg', dpi=100)
    buf.seek(0)
    imageBase64 = base64.b64encode(buf.getvalue())
    buf.close()
    return imageBase64

def create_bar(data, type_class=1):
    data_tmp_1 = list(data[0].values())[1:]
    data_tmp_2 = list(data[5].values())[1:]
    data1 = data_tmp_1
    data2 = data_tmp_2
    year = ["N+1", "N+2", "N+3", "N+4", "N+5","N+6","N+7","N+8","N+9","N+10"]
    fig, ax = plt.subplots()
    width = 0.5
    rects1 = ax.bar(year, data1, width, color="green", label="Chiffre d'affaire")
    rects2 = ax.bar(year, data2, width, color="yellow", bottom=np.array(data1), label="Achats consommés")

    ax.legend(loc="lower left", bbox_to_anchor=(0.8, 1.0))
    fig.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='jpeg', dpi=100)
    buf.seek(0)
    imageBase64 = base64.b64encode(buf.getvalue())
    buf.close()
    return imageBase64

def create_bar2(data, type_class=1):
    data_tmp_1 = list(data[0].values())[1:]
    data_tmp_2 = list(data[10].values())[1:]
    data_tmp_3 = list(data[18].values())[1:]
    
    data1 = np.array(data_tmp_1)  # Chiffre d'affaire
    data2 = np.array(data_tmp_2)  # EBE
    data3 = np.array(data_tmp_3)  # Resultat Net

    year = ["N+1", "N+2", "N+3", "N+4", "N+5", "N+6", "N+7", "N+8", "N+9", "N+10"]

    fig, ax = plt.subplots()
    width = 0.5
    
    rects1 = ax.bar(year, data1, width, color="green", label="Chiffre d'affaire")
    rects2 = ax.bar(year, data2, width, color="yellow", bottom=data1, label="EBE")
    rects3 = ax.bar(year, data3, width, color="blue", bottom=data1 + data2, label="Resultat Net")

    ax.legend(loc="lower left", bbox_to_anchor=(0.8, 1.0))
    fig.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='jpeg', dpi=100)
    buf.seek(0)
    imageBase64 = base64.b64encode(buf.getvalue())
    buf.close()

    return imageBase64

def get_amount(line_ids, ratio_ids, index, is_prev=0):
    chiffre_daffaire = line_ids.filtered(lambda r: r.poste_comptable == '1')
    amount_n = amount_n1 = amount_n2 = amount_n3 = amount_n4 = amount_n5 = amount_n6 = amount_n7 = amount_n8 = amount_n9 = amount_n10 = 0.00

    if index == "1":
        achat_consomme = line_ids.filtered(lambda r: r.poste_comptable == '6')
        amount_n = chiffre_daffaire.amount_n - achat_consomme.amount_n
        amount_n1 = chiffre_daffaire.amount_n1 - achat_consomme.amount_n1
        amount_n2 = chiffre_daffaire.amount_n2 - achat_consomme.amount_n2
        amount_n3 = chiffre_daffaire.amount_n3 - achat_consomme.amount_n3
        amount_n6 = chiffre_daffaire.amount_n6 - achat_consomme.amount_n6
        amount_n7 = chiffre_daffaire.amount_n7 - achat_consomme.amount_n7
        amount_n8 = chiffre_daffaire.amount_n8 - achat_consomme.amount_n8
        amount_n9 = chiffre_daffaire.amount_n8 - achat_consomme.amount_n9
        if is_prev != 0:
            amount_n4 = chiffre_daffaire.amount_n4 - achat_consomme.amount_n4
            amount_n5 = chiffre_daffaire.amount_n5 - achat_consomme.amount_n5
            
           

    elif index == "2":
        marge = ratio_ids.filtered(lambda r: r.ratio == '1')
        amount_n = (marge.amount_n / chiffre_daffaire.amount_n) * 100 if chiffre_daffaire.amount_n > 0 else 0
        amount_n1 = (marge.amount_n1 / chiffre_daffaire.amount_n1) * 100 if chiffre_daffaire.amount_n1 > 0 else 0
        amount_n2 = (marge.amount_n2 / chiffre_daffaire.amount_n2) * 100 if chiffre_daffaire.amount_n2 > 0 else 0
        amount_n3 = (marge.amount_n3 / chiffre_daffaire.amount_n3) * 100 if chiffre_daffaire.amount_n3 > 0 else 0
        amount_n6 = (marge.amount_n6 / chiffre_daffaire.amount_n6) * 100 if chiffre_daffaire.amount_n6 > 0 else 0
        amount_n7 = (marge.amount_n7 / chiffre_daffaire.amount_n7) * 100 if chiffre_daffaire.amount_n7 > 0 else 0
        amount_n8 = (marge.amount_n8 / chiffre_daffaire.amount_n8) * 100 if chiffre_daffaire.amount_n8 > 0 else 0
        amount_n9 = (marge.amount_n8 / chiffre_daffaire.amount_n9) * 100 if chiffre_daffaire.amount_n9 > 0 else 0
        if is_prev != 0:
            amount_n4 = (marge.amount_n4 / chiffre_daffaire.amount_n4) * 100 if chiffre_daffaire.amount_n4 > 0 else 0
            amount_n5 = (marge.amount_n5 / chiffre_daffaire.amount_n5) * 100 if chiffre_daffaire.amount_n5 > 0 else 0
            
            

    elif index == "3":
        EBE = line_ids.filtered(lambda r: r.poste_comptable == '11')
        amount_n = (EBE.amount_n / chiffre_daffaire.amount_n) * 100 if chiffre_daffaire.amount_n > 0 else 0
        amount_n1 = (EBE.amount_n1 / chiffre_daffaire.amount_n1) * 100 if chiffre_daffaire.amount_n1 > 0 else 0
        amount_n2 = (EBE.amount_n2 / chiffre_daffaire.amount_n2) * 100 if chiffre_daffaire.amount_n2 > 0 else 0
        amount_n3 = (EBE.amount_n3 / chiffre_daffaire.amount_n3) * 100 if chiffre_daffaire.amount_n3 > 0 else 0
        amount_n6 = (EBE.amount_n6 / chiffre_daffaire.amount_n6) * 100 if chiffre_daffaire.amount_n6 > 0 else 0
        amount_n7 = (EBE.amount_n7 / chiffre_daffaire.amount_n7) * 100 if chiffre_daffaire.amount_n7 > 0 else 0
        amount_n8 = (EBE.amount_n8 / chiffre_daffaire.amount_n8) * 100 if chiffre_daffaire.amount_n8 > 0 else 0
        amount_n9 = (EBE.amount_n8 / chiffre_daffaire.amount_n9) * 100 if chiffre_daffaire.amount_n9 > 0 else 0
        if is_prev != 0:
            amount_n4 = (EBE.amount_n4 / chiffre_daffaire.amount_n4) * 100 if chiffre_daffaire.amount_n4 > 0 else 0
            amount_n5 = (EBE.amount_n5 / chiffre_daffaire.amount_n5) * 100 if chiffre_daffaire.amount_n5 > 0 else 0
            
    return [amount_n, amount_n1, amount_n2, amount_n3, amount_n4, amount_n5,amount_n6,amount_n7,amount_n8,amount_n9]


def get_data(data, type_class=1):
    recordset = []
    if type_class != 1:
        for i in data:
            element = {
                'poste_comptable': TCR_LIST[int(i.poste_comptable) - 1][1],
                'amount_n': i.amount_n,
                'amount_n1': i.amount_n1,
                'amount_n2': i.amount_n2,
                'amount_n3': i.amount_n3,
                'amount_n4': i.amount_n4,
                'amount_n5': i.amount_n5,
                'amount_n6': i.amount_n6,
                'amount_n7': i.amount_n7,
                'amount_n8': i.amount_n8,
                'amount_n9': i.amount_n9,
                
            }
            recordset.append(element)
    else:
        for i in data:
            element = {
                'poste_comptable': TCR_LIST[int(i.poste_comptable) - 1][1],
                'amount_n1': i.amount_n1,
                'amount_n2': i.amount_n2,
                'amount_n3': i.amount_n3,
                'amount_n4': i.amount_n4,
                'amount_n5': i.amount_n5,
                'amount_n6': i.amount_n6,
                'amount_n7': i.amount_n7,
                'amount_n8': i.amount_n8,
                'amount_n9': i.amount_n9,
                
            }
            recordset.append(element)
    return recordset

def calculFormule(line_ids):
    calcul = line_ids.filtered(lambda r: r.poste_comptable == '1')
    valeurs = line_ids.filtered(lambda r: r.poste_comptable in ['2', '3', '4', '5'])
    calcul.amount_n = sum(valeurs.mapped('amount_n'))
    calcul.amount_n1 = sum(valeurs.mapped('amount_n1'))
    calcul.amount_n2 = sum(valeurs.mapped('amount_n2'))
    calcul.amount_n3 = sum(valeurs.mapped('amount_n3'))
    calcul.amount_n4 = sum(valeurs.mapped('amount_n4'))
    calcul.amount_n5 = sum(valeurs.mapped('amount_n5'))
    calcul.amount_n6 = sum(valeurs.mapped('amount_n6'))
    calcul.amount_n7 = sum(valeurs.mapped('amount_n7'))
    calcul.amount_n8 = sum(valeurs.mapped('amount_n8'))
    calcul.amount_n9 = sum(valeurs.mapped('amount_n9'))
  
    
    calcul1 = line_ids.filtered(lambda r: r.poste_comptable == '8')
    valeurs = line_ids.filtered(lambda r: r.poste_comptable in ['6', '7'])
    calcul1.amount_n = calcul.amount_n - sum(valeurs.mapped('amount_n'))
    calcul1.amount_n1 = calcul.amount_n1 - sum(valeurs.mapped('amount_n1'))
    calcul1.amount_n2 = calcul.amount_n2 - sum(valeurs.mapped('amount_n2'))
    calcul1.amount_n3 = calcul.amount_n3 - sum(valeurs.mapped('amount_n3'))
    calcul1.amount_n4 = calcul.amount_n4 - sum(valeurs.mapped('amount_n4'))
    calcul1.amount_n5 = calcul.amount_n5 - sum(valeurs.mapped('amount_n5'))
    calcul1.amount_n6 = calcul.amount_n6 - sum(valeurs.mapped('amount_n6'))
    calcul1.amount_n7 = calcul.amount_n7 - sum(valeurs.mapped('amount_n7'))
    calcul1.amount_n8 = calcul.amount_n8 - sum(valeurs.mapped('amount_n8'))
    calcul1.amount_n9 = calcul.amount_n9 - sum(valeurs.mapped('amount_n9'))
  
    
    calcul2 = line_ids.filtered(lambda r: r.poste_comptable == '11')
    valeurs = line_ids.filtered(lambda r: r.poste_comptable in ['9', '10'])
    calcul2.amount_n = calcul1.amount_n - sum(valeurs.mapped('amount_n'))
    calcul2.amount_n1 = calcul1.amount_n1 - sum(valeurs.mapped('amount_n1'))
    calcul2.amount_n2 = calcul1.amount_n2 - sum(valeurs.mapped('amount_n2'))
    calcul2.amount_n3 = calcul1.amount_n3 - sum(valeurs.mapped('amount_n3'))
    calcul2.amount_n4 = calcul1.amount_n4 - sum(valeurs.mapped('amount_n4'))
    calcul2.amount_n5 = calcul1.amount_n5 - sum(valeurs.mapped('amount_n5'))
    calcul2.amount_n6 = calcul1.amount_n6 - sum(valeurs.mapped('amount_n6'))
    calcul2.amount_n7 = calcul1.amount_n7 - sum(valeurs.mapped('amount_n7'))
    calcul2.amount_n8 = calcul1.amount_n8 - sum(valeurs.mapped('amount_n8'))
    calcul2.amount_n9 = calcul1.amount_n9 - sum(valeurs.mapped('amount_n9'))
    
    
    return line_ids