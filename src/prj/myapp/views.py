from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Avg, Sum, F, Q, DecimalField
from django.db.models.functions import Coalesce
from django.db import transaction
from .models import *
from openpyxl import load_workbook, Workbook
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from io import BytesIO
from datetime import datetime, timedelta
from datetime import date
import calendar
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Sum, Avg, F, DecimalField
from django.db.models.functions import Coalesce
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from datetime import datetime, date
import calendar
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Sum, Avg, F, DecimalField
from django.db.models.functions import Coalesce
from decimal import Decimal
from datetime import datetime
import calendar
from django.db.models import Count

from .models import ProductType, Product, CartProducts, ProductPrice

from django.contrib.auth.decorators import login_required
import io
import base64
import matplotlib
matplotlib.use('Agg') 
# ====================
# Chart Generation
# ====================
def get_inpc_chart_data():
    today = datetime.now()
    last_6_months = []
    current_year = today.year
    current_month = today.month

    for i in range(6):
        mo = current_month - i
        yr = current_year
        if mo <= 0:
            mo += 12
            yr -= 1
        last_6_months.append((yr, mo))

    inpc_data = []
    for (yr, mo) in reversed(last_6_months):
        inpc_value = calculer_inpc_global_mensuel(annee=yr, mois=mo)
        inpc_data.append({
            'year': yr,
            'month': mo,
            'month_name': calendar.month_name[mo],
            'inpc': inpc_value
        })

    return inpc_data
def calculer_inpc_global_mensuel(annee, mois):
    """
    Calcule l'Indice National des Prix à la Consommation (INPC) pour un mois et une année donnés.

    Args:
        annee (int): L'année pour laquelle calculer l'INPC.
        mois (int): Le mois pour lequel calculer l'INPC.

    Returns:
        Decimal: La valeur de l'INPC calculée.
    """
    prix_entries = ProductPrice.objects.filter(
        date_from__year=annee,
        date_from__month=mois
    )

    # Calcul de la somme des pondérations via la relation produit -> CartProducts
    somme_ponderations = prix_entries.aggregate(
        total_pond=Coalesce(Sum('product__cartproducts__weight'), Decimal('0.00'))
    )['total_pond']

    # Calcul de la somme des produits pondérés (prix * pondération)
    somme_produits_ponderees = prix_entries.aggregate(
        total_pondere=Coalesce(
            Sum(F('value') * F('product__cartproducts__weight'), output_field=DecimalField()),
            Decimal('0.00')
        )
    )['total_pondere']

    # Calcul de l'INPC en pourcentage
    inpc = (somme_produits_ponderees / somme_ponderations * Decimal('100')) if somme_ponderations > 0 else Decimal('0.00')
    return inpc
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Sum, Avg
from datetime import datetime
import calendar
from decimal import Decimal
from django.db.models.functions import Coalesce
from django.db.models import DecimalField

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg
from datetime import datetime
import calendar
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
import json

@login_required
def home_view(request):
    """
    Génère le tableau de bord interactif avec les statistiques et graphiques Django-ChartJS.
    """
    today = datetime.now()

    # 🔹 Générer la liste des 6 derniers mois
    last_6_months = [(today.year, today.month - i) for i in range(6)]
    last_6_months = [(yr - 1, mo + 12) if mo <= 0 else (yr, mo) for yr, mo in last_6_months]
    
    inpc_data = []
    for (yr, mo) in reversed(last_6_months):
        inpc_value = calculer_inpc_global_mensuel(annee=yr, mois=mo)
        inpc_data.append({
            'year': yr,
            'month': mo,
            'month_name': calendar.month_name[mo],
            'inpc': round(inpc_value, 2)
        })

    # 🔹 Calcul des statistiques globales
    total_products_calculated = Product.objects.count()
    total_weights = CartProducts.objects.aggregate(total_weight=Sum('weight'))['total_weight'] or Decimal('0.00')
    inpc_global = calculer_inpc_global_mensuel(today.year, today.month) or Decimal('0.00')
    average_inpc_6_months = sum(item['inpc'] for item in inpc_data) / len(inpc_data) if inpc_data else Decimal('0.00')

    # 📊 Préparer les données pour les graphiques
    products_by_type = Product.objects.values('product_type__label').annotate(count=Count('id'))
    product_type_distribution = ProductType.objects.annotate(num_products=Count('product'))
    avg_price_by_product_type = ProductPrice.objects.values('product__product_type__label').annotate(avg_price=Avg('value'))
    pos_by_commune = PointOfSale.objects.values('commune__name').annotate(count=Count('id'))
    total_weight_by_cart = CartProducts.objects.values('cart__name').annotate(total_weight=Sum('weight'))

    chart_data = {
        'inpc_trends': {
            'labels': [item['month_name'] for item in inpc_data],
            'data': [item['inpc'] for item in inpc_data],
        },
        'products_by_type': {
            'labels': [item['product_type__label'] for item in products_by_type],
            'data': [item['count'] for item in products_by_type],
        },
        'product_type_distribution': {
            'labels': [pt.label for pt in product_type_distribution],
            'data': [pt.num_products for pt in product_type_distribution],
        },
        'avg_price_by_product_type': {
            'labels': [item['product__product_type__label'] for item in avg_price_by_product_type],
            'data': [round(item['avg_price'], 2) if item['avg_price'] else 0 for item in avg_price_by_product_type],
        },
        'pos_by_commune': {
            'labels': [item['commune__name'] for item in pos_by_commune],
            'data': [item['count'] for item in pos_by_commune],
        },
        'total_weight_by_cart': {
            'labels': [item['cart__name'] for item in total_weight_by_cart],
            'data': [round(item['total_weight'], 2) if item['total_weight'] else 0 for item in total_weight_by_cart],
        },
    }

    # 🔹 Sérialiser les données des graphiques en JSON
    chart_data_json = json.dumps(chart_data, cls=DjangoJSONEncoder)

    # 🔹 Rendre le template avec les données statistiques et graphiques
    context = {
        'inpc_data': inpc_data,
        'inpc_global': round(inpc_global, 2),
        'total_products_calculated': total_products_calculated,
        'total_weights': round(total_weights, 2),
        'average_inpc': round(average_inpc_6_months, 2),
        'chart_data': chart_data_json,  # Ajouter les données des graphiques
    }

    return render(request, 'home.html', context)


@login_required
def commune_list_view(request):
    """
    Vue unique gérant à la fois :
      - L'affichage HTML (filtrage, recherche, pagination)
      - Les appels AJAX (renvoie un JSON filtré/paginé)
      - Filtrage par wilaya / moughataa
      - Recherche par nom ou code
      - Export en Excel (format .xlsx)
    """

    # --- 1) Lecture des paramètres GET ---
    selected_wilaya = request.GET.get('wilaya', '').strip()
    selected_moughataa = request.GET.get('moughataa', '').strip()
    search = request.GET.get('search', '').strip()
    page_number = request.GET.get('page', 1)

    # Paramètre pour export Excel, ex.: ?export=excel
    export_param = request.GET.get('export', '').strip()

    # --- 2) Construction du queryset (filtrage) ---
    communes_qs = Commune.objects.all()

    if selected_wilaya:
        communes_qs = communes_qs.filter(moughataa__wilaya__code=selected_wilaya)

    if selected_moughataa:
        communes_qs = communes_qs.filter(moughataa__code=selected_moughataa)

    if search:
        communes_qs = communes_qs.filter(
            Q(name__icontains=search) | Q(code__icontains=search)
        )

    # --- 3) Export en Excel (si ?export=excel) ---
    if export_param == 'excel':
        # Crée un classeur Excel en mémoire
        wb = Workbook()
        ws = wb.active
        ws.title = "Communes"

        # En-tête
        ws.append(["ID", "Code", "Nom", "Moughataa", "Wilaya"])

        # Ajout des lignes : pas de pagination pour l'export
        for commune in communes_qs:
            ws.append([
                commune.id,
                commune.code,
                commune.name,
                commune.moughataa.name,
                commune.moughataa.wilaya.name
            ])

        # Conversion en bytes pour la réponse HTTP
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=communes.xlsx"
        response.write(output.getvalue())
        return response

    # --- 4) Sinon, on poursuit la logique standard (HTML, AJAX) ---

    # Pagination
    paginator = Paginator(communes_qs, 10)  # 10 communes par page
    page_obj = paginator.get_page(page_number)

    # Moughataas dynamiques (pour le <select>)
    if selected_wilaya:
        moughataas_qs = Moughataa.objects.filter(wilaya__code=selected_wilaya)
    else:
        moughataas_qs = Moughataa.objects.all()

    # Mode AJAX ?
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            "communes": [],
            "pagination": {
                "current_page": page_obj.number,
                "num_pages": page_obj.paginator.num_pages,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
            }
        }
        for commune in page_obj:
            data["communes"].append({
                "id": commune.id,
                "code": commune.code,
                "name": commune.name,
                "moughataa": commune.moughataa.name,
                "wilaya": commune.moughataa.wilaya.name
            })
        return JsonResponse(data, safe=False)

    # Mode HTML classique
    context = {
        'page_obj': page_obj,
        'wilayas': Wilaya.objects.all(),
        'moughataas': moughataas_qs,
        'selected_wilaya': selected_wilaya,
        'selected_moughataa': selected_moughataa,
        'search': search
    }
    return render(request, 'commune.html', context)

@login_required
def import_data_view(request):
    """
    Gère l'import des données Excel pour
    Wilaya, Moughataa, et Commune.
    """
    if request.method == "POST":
        excel_file = request.FILES.get("excel_file")
        if excel_file:
            wb = load_workbook(excel_file)
            with transaction.atomic():
                # Feuille 1 : Wilayas
                sheet_wilayas = wb["mrt_adm_adm1_2024.shp"]
                for row in sheet_wilayas.iter_rows(min_row=2, values_only=True):
                    wilaya_name = row[2]  # ADM1_EN
                    wilaya_code = row[3]  # ADM1_PCODE
                    Wilaya.objects.update_or_create(
                        code=wilaya_code,
                        defaults={"name": wilaya_name}
                    )

                # Feuille 2 : Moughataas
                sheet_moughataas = wb["mrt_adm_adm2_2024.shp"]
                for row in sheet_moughataas.iter_rows(min_row=2, values_only=True):
                    wilaya_code = row[3]       # ADM1_PCODE
                    moughataa_name = row[4]    # ADM2_EN
                    moughataa_code = row[5]    # ADM2_PCODE
                    linked_wilaya = Wilaya.objects.get(code=wilaya_code)
                    Moughataa.objects.update_or_create(
                        code=moughataa_code,
                        defaults={
                            "name": moughataa_name,
                            "wilaya": linked_wilaya
                        }
                    )

                # Feuille 3 : Communes
                sheet_communes = wb["mrt_adm_adm3_2024.shp"]
                for row in sheet_communes.iter_rows(min_row=2, values_only=True):
                    moughataa_code = row[5]  # ADM2_PCODE
                    commune_name = row[6]    # ADM3_EN
                    commune_code = row[7]    # ADM3_PCODE
                    linked_moughataa = Moughataa.objects.get(code=moughataa_code)
                    Commune.objects.update_or_create(
                        code=commune_code,
                        defaults={
                            "name": commune_name,
                            "moughataa": linked_moughataa
                        }
                    )
            # Redirection vers la liste générale des communes après import
            return redirect("commune-list")

    # Méthode GET ou si pas de fichier, on peut juste rediriger vers la liste
    return redirect("commune-list")

@login_required
def point_of_sale_list_view(request):
    """
    Affiche la liste des points de vente (PointOfSale) avec :
      - Filtrage par commune, type
      - Recherche (code ou type)
      - Pagination
      - Réponse JSON (si requête AJAX)
      - Export Excel (via ?export=excel)
    """

    # 1) Paramètres GET
    selected_commune = request.GET.get('commune', '').strip()
    selected_type = request.GET.get('type', '').strip()
    search = request.GET.get('search', '').strip()
    page_number = request.GET.get('page', 1)
    export_param = request.GET.get('export', '').strip()  # ?export=excel

    # 2) Construction du queryset (filtrage)
    pos_qs = PointOfSale.objects.all()

    if selected_commune:
        pos_qs = pos_qs.filter(commune__code=selected_commune)

    if selected_type:
        pos_qs = pos_qs.filter(type__iexact=selected_type)

    if search:
        pos_qs = pos_qs.filter(
            Q(code__icontains=search) | Q(type__icontains=search)
        )

    # 3) Export en Excel (si ?export=excel)
    if export_param == 'excel':
        # Créer le fichier Excel en mémoire
        wb = Workbook()
        ws = wb.active
        ws.title = "PointsOfSale"

        # En-têtes de colonnes
        ws.append(["ID", "Code", "Type", "GPS Lat", "GPS Lon", "Commune"])

        # On exporte l'ensemble du queryset (pas de pagination)
        for pos in pos_qs:
            commune_name = pos.commune.name if pos.commune else ""
            ws.append([
                pos.id,
                pos.code,
                pos.type,
                pos.gps_lat,
                pos.gps_lon,
                commune_name,
            ])

        # Conversion en bytes pour la réponse HTTP
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="points_of_sale.xlsx"'
        response.write(output.getvalue())
        return response

    # 4) Sinon, logique standard (HTML ou AJAX)
    paginator = Paginator(pos_qs, 10)  # 10 items par page
    page_obj = paginator.get_page(page_number)

    # Réponse AJAX (JSON)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            "points_of_sale": [],
            "pagination": {
                "current_page": page_obj.number,
                "num_pages": page_obj.paginator.num_pages,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
            }
        }
        for pos in page_obj.object_list:
            data["points_of_sale"].append({
                "id": pos.id,
                "code": pos.code,
                "type": pos.type,
                "gps_lat": pos.gps_lat,
                "gps_lon": pos.gps_lon,
                "commune": pos.commune.name if pos.commune else "",
            })
        return JsonResponse(data, safe=False)

    # Réponse HTML classique
    communes_list = Commune.objects.all().order_by("name")
    types_list = (PointOfSale.objects
                  .values_list("type", flat=True)
                  .distinct()
                  .order_by("type"))

    context = {
        "page_obj": page_obj,
        "communes": communes_list,
        "available_types": types_list,
        "selected_commune": selected_commune,
        "selected_type": selected_type,
        "search": search,
    }
    return render(request, "pointofsale_list.html", context)

@login_required
def import_point_of_sale_view(request):
    """
    Gère l'import Excel pour PointOfSale.
    Suppose qu'on lit un fichier avec colonnes :
      Code | Type | GPS_Lat | GPS_Lon | Commune_Code
    """
    if request.method == "POST":
        excel_file = request.FILES.get("excel_file")
        if not excel_file:
            messages.error(request, "Aucun fichier sélectionné.")
            return redirect("pointofsale-list")

        try:
            wb = load_workbook(excel_file)
            sheet = wb.active  # ou wb["SheetName"] si nécessaire

            with transaction.atomic():
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    if not row:
                        continue  # ligne vide

                    code = row[0]
                    pos_type = row[1]
                    gps_lat = row[2]
                    gps_lon = row[3]
                    commune_code = row[4]

                    # Vérification de la commune
                    commune_obj = None
                    if commune_code:
                        commune_obj = Commune.objects.get(code=commune_code)

                    # Mise à jour ou création
                    PointOfSale.objects.update_or_create(
                        code=code,
                        defaults={
                            "type": pos_type,
                            "gps_lat": gps_lat,
                            "gps_lon": gps_lon,
                            "commune": commune_obj
                        }
                    )
            messages.success(request, "Importation réussie.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'import : {e}")

    # Redirection vers la liste
    return redirect("pointofsale-list")

class PointOfSaleDetailView(DetailView):
    model = PointOfSale
    template_name = 'pointofsale-detail.html'
    context_object_name = 'pointVente'


class PointOfSaleCreateView(CreateView):
    model = PointOfSale
    fields = ['code', 'type', 'gps_lat', 'gps_lon', 'commune']
    template_name = 'pointofsale-form.html'
    success_url = reverse_lazy('pointofsale-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Récupérer les types distincts pour la liste déroulante
        context['point_of_sale_types'] = PointOfSale.objects.values_list('type', flat=True).distinct()
        return context



class PointOfSaleUpdateView(UpdateView):
    model = PointOfSale
    fields = ['code', 'type', 'gps_lat', 'gps_lon', 'commune']
    template_name = 'pointofsale-form.html'
    success_url = reverse_lazy('pointofsale-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['point_of_sale_types'] = PointOfSale.objects.values_list('type', flat=True).distinct()
        return context


class PointOfSaleDeleteView(DeleteView):
    model = PointOfSale
    template_name = 'pointofsale-confirm-delete.html'
    success_url = reverse_lazy('pointofsale-list')

# ====================
# Product Views
# ====================
@login_required
def product_list_view(request):
    """
    Affiche la liste des produits (Product) avec :
      - Filtrage par product_type
      - Recherche (code, name, product_type)
      - Pagination
      - Export Excel (via ?export=excel)
      - Réponse JSON (si requête AJAX)
    """

    # 1) Paramètres GET
    selected_type = request.GET.get('product_type', '').strip()
    search = request.GET.get('search', '').strip()
    page_number = request.GET.get('page', 1)
    export_param = request.GET.get('export', '').strip()  # ?export=excel

    # 2) Construction du queryset (filtrage)
    products_qs = Product.objects.all()

    if selected_type:
        products_qs = products_qs.filter(product_type__iexact=selected_type)

    if search:
        # Recherche sur code, name, product_type
        products_qs = products_qs.filter(
            Q(code__icontains=search) |
            Q(name__icontains=search) |
            Q(product_type__icontains=search)
        )

    # 3) Export en Excel (si ?export=excel)
    if export_param == 'excel':
        wb = Workbook()
        ws = wb.active
        ws.title = "Products"

        # Entêtes de colonnes
        ws.append(["ID", "Code", "Name", "Description", "Unit Measure", "Product Type"])

        # Pas de pagination pour l'export : on exporte TOUT le queryset filtré
        for prod in products_qs:
            ws.append([
                prod.id,
                prod.code,
                prod.name,
                prod.description,
                prod.unit_measure,
                prod.product_type
            ])

        output = BytesIO()
        wb.save(output)
        output.seek(0)

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="products.xlsx"'
        response.write(output.getvalue())
        return response

    # 4) Mode normal (HTML ou AJAX)
    paginator = Paginator(products_qs, 10)  # 10 produits par page
    page_obj = paginator.get_page(page_number)

    # Mode AJAX => JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            "products": [],
            "pagination": {
                "current_page": page_obj.number,
                "num_pages": page_obj.paginator.num_pages,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
            }
        }
        for product in page_obj.object_list:
            data["products"].append({
                "id": product.id,
                "code": product.code,
                "name": product.name,
                "description": product.description,
                "unit_measure": product.unit_measure,
                "product_type": product.product_type,
            })
        return JsonResponse(data, safe=False)

    # Liste des types disponibles (distinct)
    product_types_list = (Product.objects
                          .values_list("product_type", flat=True)
                          .distinct()
                          .order_by("product_type"))

    context = {
        "page_obj": page_obj,
        "product_types": product_types_list,
        "selected_type": selected_type,
        "search": search
    }
    return render(request, "product_list.html", context)
@login_required
def import_product_view(request):
    """
    Gère l'import Excel pour Product.
    Suppose qu'on lit un fichier avec colonnes :
      code | name | description | unit_measure | product_type_code
      (ligne d'en-tête ignorée, min_row=2)
    """
    if request.method == "POST":
        excel_file = request.FILES.get("excel_file")
        if not excel_file:
            messages.error(request, "Aucun fichier sélectionné.")
            return redirect("product-list")

        try:
            wb = load_workbook(excel_file)
            sheet = wb.active  # ou wb["NomDeFeuille"] si besoin

            with transaction.atomic():
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    if not row:
                        continue  # ligne vide
                    code = row[0]
                    name = row[1]
                    description = row[2]
                    unit_measure = row[3]
                    product_type_code = row[4]  # Assurez-vous que c'est le code, pas le label

                    # Récupérer le ProductType correspondant
                    try:
                        product_type = ProductType.objects.get(code=product_type_code)
                    except ProductType.DoesNotExist:
                        messages.error(request, f"Type de produit '{product_type_code}' introuvable pour le produit '{code}'.")
                        continue  # Aller à la ligne suivante

                    # Mise à jour ou création
                    Product.objects.update_or_create(
                        code=code,
                        defaults={
                            "name": name,
                            "description": description,
                            "unit_measure": unit_measure,
                            "product_type": product_type  # Assigner l'objet ProductType
                        }
                    )
            messages.success(request, "Importation réussie.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'import : {e}")

    return redirect("product-list")

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product-detail.html'

class ProductCreateView(CreateView):
    model = Product
    fields = ['code', 'name', 'description', 'unit_measure', 'product_type']
    template_name = 'product-form.html'
    success_url = reverse_lazy('product-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passer tous les types de produits au template
        context['product_types'] = ProductType.objects.all()
        return context


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['code', 'name', 'description', 'unit_measure', 'product_type']
    template_name = 'product-form.html'
    success_url = reverse_lazy('product-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_types'] = ProductType.objects.all()  # Correctement indenté
        return context

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product-confirm-delete.html'
    success_url = reverse_lazy('product-list')


# ====================
# Product Price Views
# ====================
@login_required
def productprice_list_view(request):
    """
    Affiche la liste des prix des produits (ProductPrice) avec :
      - Filtrage (ex. par product, par point_of_sale)
      - Recherche
      - Export Excel (si ?export=excel)
      - Pagination
      - Réponse JSON (si AJAX)
    """

    # 1) Lecture des paramètres GET
    selected_product = request.GET.get("product", "").strip()
    selected_pos = request.GET.get("point_of_sale", "").strip()
    search = request.GET.get("search", "").strip()
    page_number = request.GET.get("page", 1)
    export_param = request.GET.get("export", "").strip()  # ?export=excel

    # 2) Construction du queryset (filtrage)
    pp_qs = ProductPrice.objects.select_related("product", "point_of_sale").all()

    # Filtrage par produit (selon ID ou code)
    if selected_product:
        # si vous avez un champ "code" ou "id" => ajustez
        pp_qs = pp_qs.filter(product__id=selected_product)

    # Filtrage par point de vente
    if selected_pos:
        pp_qs = pp_qs.filter(point_of_sale__id=selected_pos)

    # Recherche globale
    if search:
        # Filtre sur product.name, point_of_sale.type ou code, etc.
        pp_qs = pp_qs.filter(
            Q(product__name__icontains=search) |
            Q(point_of_sale__type__icontains=search)
        )

    # 3) Export Excel si ?export=excel
    if export_param == "excel":
        wb = Workbook()
        ws = wb.active
        ws.title = "ProductPrices"

        # En-têtes de colonnes
        ws.append(["ID", "Produit", "Point de Vente", "Prix", "Date Début", "Date Fin"])

        # Pas de pagination pour l'export
        for pp in pp_qs:
            product_name = pp.product.name if pp.product else ""
            pos_name = pp.point_of_sale.type if pp.point_of_sale else ""
            date_from = pp.date_from.strftime("%Y-%m-%d") if pp.date_from else ""
            date_to = pp.date_to.strftime("%Y-%m-%d") if pp.date_to else ""

            ws.append([
                pp.id,
                product_name,
                pos_name,
                pp.value,
                date_from,
                date_to,
            ])

        output = BytesIO()
        wb.save(output)
        output.seek(0)

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="product_prices.xlsx"'
        response.write(output.getvalue())
        return response

    # 4) Sinon, logique standard (HTML / AJAX)
    paginator = Paginator(pp_qs, 10)
    page_obj = paginator.get_page(page_number)

    # Mode AJAX => JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            "product_prices": [],
            "pagination": {
                "current_page": page_obj.number,
                "num_pages": page_obj.paginator.num_pages,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
            }
        }
        for pp in page_obj:
            data["product_prices"].append({
                "id": pp.id,
                "product_name": pp.product.name if pp.product else "",
                "point_of_sale": pp.point_of_sale.type if pp.point_of_sale else "",
                "value": pp.value,
                "date_from": pp.date_from.isoformat() if pp.date_from else None,
                "date_to": pp.date_to.isoformat() if pp.date_to else None
            })
        return JsonResponse(data, safe=False)

    # Mode HTML
    context = {
        "page_obj": page_obj,
        "search": search,
        "selected_product": selected_product,
        "selected_pos": selected_pos
    }
    return render(request, "productprice_list.html", context)
@login_required
def import_productprice_view(request):
    """
    Gère l'import Excel pour ProductPrice.
    Suppose qu'on lit un fichier avec colonnes :
      product_code | pointofsale_code | value | date_from | date_to
    (adapter selon votre vrai fichier)
    """

    if request.method == "POST":
        excel_file = request.FILES.get("excel_file")
        if not excel_file:
            messages.error(request, "Aucun fichier sélectionné.")
            return redirect("productprice-list")

        try:
            wb = load_workbook(excel_file)
            sheet = wb.active  # ou wb["SheetName"] si besoin

            with transaction.atomic():
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    if not row:
                        continue

                    product_code = row[0]
                    pos_code = row[1]
                    value_price = row[2]
                    date_from_val = row[3]
                    date_to_val = row[4]

                    # Récupérer le Product
                    product_obj = None
                    if product_code:
                        product_obj = Product.objects.get(code=product_code)

                    # Récupérer le PointOfSale
                    pos_obj = None
                    if pos_code:
                        pos_obj = PointOfSale.objects.get(code=pos_code)

                    # Mise à jour / création
                    # Hypothèse : un ProductPrice est identifié par (product, point_of_sale, date_from ?)
                    ProductPrice.objects.update_or_create(
                        product=product_obj,
                        point_of_sale=pos_obj,
                        date_from=date_from_val,
                        defaults={
                            "value": value_price,
                            "date_to": date_to_val
                        }
                    )
            messages.success(request, "Importation réussie.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'import : {e}")

    return redirect("productprice-list")
class ProductPriceDetailView(DetailView):
    model = ProductPrice
    template_name = 'productprice-detail.html'

class ProductPriceCreateView(CreateView):
    model = ProductPrice
    fields = '__all__'
    template_name = 'productprice-form.html'
    success_url = reverse_lazy('productprice-list')

class ProductPriceUpdateView(UpdateView):
    model = ProductPrice
    fields = '__all__'
    template_name = 'productprice-form.html'
    success_url = reverse_lazy('productprice-list')

class ProductPriceDeleteView(DeleteView):
    model = ProductPrice
    template_name = 'productprice-confirm-delete.html'
    success_url = reverse_lazy('productprice-list')


# ====================
# Cart Views
# ====================
@login_required
def cart_list_view(request):
    """
    Affiche la liste des paniers (Cart) avec :
      - Filtrage (exemple : recherche par code ou nom)
      - Export Excel (si ?export=excel)
      - Pagination
      - Réponse JSON (si AJAX)
    """

    # 1) Lecture des paramètres GET
    search = request.GET.get('search', '').strip()
    page_number = request.GET.get('page', 1)
    export_param = request.GET.get('export', '').strip()  # ex: ?export=excel

    # 2) Construction du queryset
    carts_qs = Cart.objects.all()

    # Filtrage (recherche simple sur code ou nom)
    if search:
        carts_qs = carts_qs.filter(
            Q(code__icontains=search) |
            Q(name__icontains=search)
        )

    # 3) Export Excel
    if export_param == 'excel':
        wb = Workbook()
        ws = wb.active
        ws.title = "Carts"

        # En-têtes
        ws.append(["ID", "Code", "Name", "Description"])

        # Export complet, sans pagination
        for cart in carts_qs:
            ws.append([
                cart.id,
                cart.code,
                cart.name,
                cart.description
            ])

        output = BytesIO()
        wb.save(output)
        output.seek(0)

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="carts.xlsx"'
        response.write(output.getvalue())
        return response

    # 4) Logique standard (HTML ou AJAX)
    paginator = Paginator(carts_qs, 10)  # 10 paniers par page
    page_obj = paginator.get_page(page_number)

    # Mode AJAX => renvoyer JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            "carts": [],
            "pagination": {
                "current_page": page_obj.number,
                "num_pages": page_obj.paginator.num_pages,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
            }
        }
        for cart in page_obj:
            data["carts"].append({
                "id": cart.id,
                "code": cart.code,
                "name": cart.name,
                "description": cart.description
            })
        return JsonResponse(data, safe=False)

    # Mode HTML classique
    context = {
        'carts': page_obj,     # vous pouvez nommer 'carts' ou 'page_obj' selon votre template
        'search': search
    }
    return render(request, 'cart_list.html', context)
@login_required
def import_cart_view(request):
    """
    Gère l'import Excel pour Cart.
    Suppose que le fichier Excel a des colonnes :
      code | name | description
      (Ligne d'en-tête ignorée, on commence à la ligne 2)
    """
    if request.method == "POST":
        excel_file = request.FILES.get("excel_file")
        if not excel_file:
            messages.error(request, "Aucun fichier sélectionné.")
            return redirect("cart-list")

        try:
            wb = load_workbook(excel_file)
            sheet = wb.active  # ou wb["SheetName"] si vous avez une feuille nommée

            with transaction.atomic():
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    if not row:
                        continue  # ignore les lignes vides
                    code = row[0]
                    name = row[1]
                    description = row[2]

                    # Création / Mise à jour
                    Cart.objects.update_or_create(
                        code=code,
                        defaults={
                            "name": name,
                            "description": description
                        }
                    )
            messages.success(request, "Importation réussie.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'import : {e}")

    return redirect("cart-list")

class CartDetailView(DetailView):
    model = Cart
    template_name = 'cart-detail.html'

class CartCreateView(CreateView):
    model = Cart
    fields = '__all__'
    template_name = 'cart-form.html'
    success_url = reverse_lazy('cart-list')

class CartUpdateView(UpdateView):
    model = Cart
    fields = '__all__'
    template_name = 'cart-form.html'
    success_url = reverse_lazy('cart-list')

class CartDeleteView(DeleteView):
    model = Cart
    template_name = 'cart-confirm-delete.html'
    success_url = reverse_lazy('cart-list')


# ====================
# Cart Products Views
# ====================
@login_required
def cartproducts_list_view(request):
    """
    Affiche la liste des produits dans les paniers (CartProducts) avec :
      - Filtrage (ex. search par product name / cart name)
      - Export Excel (si ?export=excel)
      - Pagination
      - Réponse JSON (si AJAX)
    """

    # 1) Paramètres GET
    search = request.GET.get('search', '').strip()
    page_number = request.GET.get('page', 1)
    export_param = request.GET.get('export', '').strip()  # ?export=excel

    # 2) Construction du queryset
    cartprod_qs = CartProducts.objects.select_related('product', 'cart').all()

    # Filtrage / Recherche simple
    if search:
        cartprod_qs = cartprod_qs.filter(
            Q(product__name__icontains=search) |
            Q(cart__name__icontains=search)
        )

    # 3) Export Excel (si ?export=excel)
    if export_param == 'excel':
        wb = Workbook()
        ws = wb.active
        ws.title = "CartProducts"

        # Entêtes de colonnes (selon votre modèle)
        ws.append(["ID", "Produit", "Panier", "Poids", "Date d'ajout", "Date de fin"])

        # Pas de pagination pour l’export
        for cp in cartprod_qs:
            ws.append([
                cp.id,
                cp.product.name if cp.product else "",
                cp.cart.name if cp.cart else "",
                cp.weight if cp.weight else "",
                cp.date_from.strftime("%Y-%m-%d") if cp.date_from else "",
                cp.date_to.strftime("%Y-%m-%d") if cp.date_to else "",
            ])

        output = BytesIO()
        wb.save(output)
        output.seek(0)

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="cart_products.xlsx"'
        response.write(output.getvalue())
        return response

    # 4) Mode standard (HTML ou AJAX)
    paginator = Paginator(cartprod_qs, 10)  # 10 items par page
    page_obj = paginator.get_page(page_number)

    # Si AJAX => JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            "cart_products": [],
            "pagination": {
                "current_page": page_obj.number,
                "num_pages": page_obj.paginator.num_pages,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
            }
        }
        for cp in page_obj:
            data["cart_products"].append({
                "id": cp.id,
                "product": cp.product.name if cp.product else "",
                "cart": cp.cart.name if cp.cart else "",
                "weight": cp.weight,
                "date_from": cp.date_from.isoformat() if cp.date_from else None,
                "date_to": cp.date_to.isoformat() if cp.date_to else None
            })
        return JsonResponse(data, safe=False)

    # Rendu HTML classique
    context = {
        "cart_products": page_obj,
        "search": search,
    }
    return render(request, "cartproducts_list.html", context)

@login_required
def import_cartproducts_view(request):
    """
    Gère l'import Excel pour CartProducts.
    Suppose qu'on lit un fichier avec colonnes :
      product_code | cart_code | weight | date_from | date_to
    (adapter selon votre vrai fichier)
    """

    if request.method == "POST":
        excel_file = request.FILES.get("excel_file")
        if not excel_file:
            messages.error(request, "Aucun fichier sélectionné.")
            return redirect("cartproducts-list")

        try:
            wb = load_workbook(excel_file)
            sheet = wb.active  # ou wb["SheetName"] si nécessaire

            with transaction.atomic():
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    if not row:
                        continue  # ligne vide

                    product_code = row[0]
                    cart_code = row[1]
                    weight_val = row[2]
                    date_from_val = row[3]
                    date_to_val = row[4]

                    # Récupération du Product
                    product_obj = None
                    if product_code:
                        product_obj = Product.objects.get(code=product_code)

                    # Récupération du Cart
                    cart_obj = None
                    if cart_code:
                        cart_obj = Cart.objects.get(code=cart_code)

                    # Création / mise à jour
                    # Hypothèse : un CartProducts est unique par (product, cart) ?
                    CartProducts.objects.update_or_create(
                        product=product_obj,
                        cart=cart_obj,
                        defaults={
                            "weight": weight_val,
                            "date_from": date_from_val,
                            "date_to": date_to_val
                        }
                    )
            messages.success(request, "Importation réussie.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'import : {e}")

    # Redirection vers la liste
    return redirect("cartproducts-list")

class CartProductsDetailView(DetailView):
    model = CartProducts
    template_name = 'cartproducts-detail.html'

class CartProductsCreateView(CreateView):
    model = CartProducts
    fields = '__all__'
    template_name = 'cartproducts-form.html'
    success_url = reverse_lazy('cartproducts-list')

class CartProductsUpdateView(UpdateView):
    model = CartProducts
    fields = '__all__'
    template_name = 'cartproducts-form.html'
    success_url = reverse_lazy('cartproducts-list')

class CartProductsDeleteView(DeleteView):
    model = CartProducts
    template_name = 'cartproducts-confirm-delete.html'
    success_url = reverse_lazy('cartproducts-list')


# =========================
# Product Type Views
# =========================
@login_required
def producttype_list_view(request):
    """
    Affiche la liste des types de produits (ProductType) avec :
      - Recherche (code, label, description)
      - Export Excel (via ?export=excel)
      - Pagination
      - Réponse JSON (si AJAX)
    """

    # 1) Paramètres GET
    search = request.GET.get('search', '').strip()
    page_number = request.GET.get('page', 1)
    export_param = request.GET.get('export', '').strip()  # ?export=excel

    # 2) Construction du queryset (filtrage)
    product_types_qs = ProductType.objects.all()

    if search:
        product_types_qs = product_types_qs.filter(
            Q(code__icontains=search) |
            Q(label__icontains=search) |
            Q(description__icontains=search)
        )

    # 3) Export en Excel (si ?export=excel)
    if export_param == 'excel':
        wb = Workbook()
        ws = wb.active
        ws.title = "ProductTypes"

        # En-têtes de colonnes
        ws.append(["ID", "Code", "Label", "Description"])

        # Pas de pagination pour l'export
        for pt in product_types_qs:
            ws.append([
                pt.id,
                pt.code,
                pt.label,
                pt.description
            ])

        output = BytesIO()
        wb.save(output)
        output.seek(0)

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="product_types.xlsx"'
        response.write(output.getvalue())
        return response

    # 4) Mode standard (HTML ou AJAX)
    paginator = Paginator(product_types_qs, 10)  # 10 types par page
    page_obj = paginator.get_page(page_number)

    # Mode AJAX => JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            "product_types": [],
            "pagination": {
                "current_page": page_obj.number,
                "num_pages": page_obj.paginator.num_pages,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
            }
        }
        for pt in page_obj:
            data["product_types"].append({
                "id": pt.id,
                "code": pt.code,
                "label": pt.label,
                "description": pt.description
            })
        return JsonResponse(data, safe=False)

    # Mode HTML
    context = {
        "page_obj": page_obj,
        "search": search
    }
    return render(request, "producttype_list.html", context)
@login_required
def import_producttype_view(request):
    """
    Gère l'import Excel pour ProductType.
    Suppose qu'on lit un fichier avec colonnes :
      code | label | description
      (ligne d'en-tête ignorée, min_row=2)
    """
    if request.method == "POST":
        excel_file = request.FILES.get("excel_file")
        if not excel_file:
            messages.error(request, "Aucun fichier sélectionné.")
            return redirect("producttype-list")

        try:
            wb = load_workbook(excel_file)
            sheet = wb.active

            with transaction.atomic():
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    if not row:
                        continue  # ligne vide
                    code, label, description = row

                    # Mise à jour ou création
                    ProductType.objects.update_or_create(
                        code=code,
                        defaults={
                            "label": label,
                            "description": description,
                        }
                    )
            messages.success(request, "Importation réussie.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'import : {e}")

    return redirect("producttype-list")

class ProductTypeDetailView(DetailView):
    model = ProductType
    template_name = 'producttype-detail.html'
    context_object_name = 'producttype'

class ProductTypeCreateView(CreateView):
    model = ProductType
    fields = ['code', 'label', 'description']
    template_name = 'producttype-form.html'
    success_url = reverse_lazy('producttype-list')

class ProductTypeUpdateView(UpdateView):
    model = ProductType
    fields = ['code', 'label', 'description']
    template_name = 'producttype-form.html'
    success_url = reverse_lazy('producttype-list')

class ProductTypeDeleteView(DeleteView):
    model = ProductType
    template_name = 'producttype-confirm-delete.html'
    success_url = reverse_lazy('producttype-list')

# myapp/views.py

