import werkzeug
from flask import render_template, request, flash
from flask_login import login_required, current_user
from werkzeug.exceptions import BadRequest
from werkzeug.utils import redirect

from service.ad_service import AdService
from service.review_service import ReviewService
from utils.forms import AdCreationForm, AdSearchForm, ReviewCreationForm, ResponseCreationForm, show_error_messages
from utils.pagination import Pagination

DEFAULT_PAGE_SIZE = 5


def show_ads():
    """
    This function implements GET /ads end point
    :returns: template with ad list, containing page of all ads
    """
    ad_number = AdService.get_ad_count()
    page = request.args.get("page", type=int, default=1)
    ads = AdService.get_ad_list(page=page, size=DEFAULT_PAGE_SIZE)
    pagination = Pagination(page=page, total_count=ad_number, page_size=DEFAULT_PAGE_SIZE)
    search_form = AdSearchForm()
    return render_template('ad_list.html', pagination=pagination, ads=ads, form=search_form)


def filter_ads():
    """This function implements GET /ads/search end point.
    :returns: template containing list of ads according to filters
    """
    search_form = AdSearchForm(request.args)
    if search_form.validate():
        page = request.args.get("page", type=int, default=1)
        ads, total = AdService.filter_ads(search_form.data, page=page, size=DEFAULT_PAGE_SIZE)
        pagination = Pagination(page=page, total_count=total, page_size=DEFAULT_PAGE_SIZE)
        return render_template('ad_list.html', pagination=pagination, ads=ads, form=search_form)
    else:
        show_error_messages(search_form)
        return redirect('ads')


@login_required
def add_ad():
    """This function implements POST /ads end point.
    :returns: redirect to /ad/<ad_id> end point
    """
    ad_form = AdCreationForm(request.form)
    if ad_form.validate():
        user_id = current_user.get_id()
        ad_id = AdService.add_ad(ad_form.data, user_id)
        return redirect(f'/ads/{ad_id}')
    else:
        show_error_messages(ad_form)
        return redirect('ads/new')


def ad_detail(ad_id):
    """This function implements GET ads/<ad_id> end point.
    :param: ad_id - id of an ad to be displayed
    :returns: template with ad details and its reviews
    """
    page = request.args.get("page", type=int, default=1)
    review_number = ReviewService.get_review_count(ad_id)
    ad, reviews = AdService.get_all_ad_detail(ad_id, page)
    review_form = ReviewCreationForm()
    response_form = ResponseCreationForm()
    pagination = Pagination(page=page, total_count=review_number, page_size=DEFAULT_PAGE_SIZE)
    if not ad:
        raise werkzeug.exceptions.NotFound
    else:
        return render_template('ad_detail.html', ad=ad, reviews=reviews, form=review_form, pagination=pagination,
                               response_form=response_form)


@login_required
def show_add_ad():
    """This function implements GET /ads/new end point
    :returns: page with ad creation form"""
    ad_form = AdCreationForm()
    return render_template('ad_add.html', form=ad_form)


@login_required
def delete_ad(ad_id):
    """This function implements POST /ads/<ad_id>/delete end point
    It deletes ad with given id.
    :returns: page with user detail"""
    user_id = current_user.get_id()
    if AdService.delete_ad(ad_id, user_id):
        flash('Usunięto')
    else:
        flash('Nie udało się usunąć')
    return redirect('/me')


@login_required
def show_edit_ad(ad_id):
    """This function implements GET /ads/<ad_id>/edit end point
    :param ad_id: id of the ad to be edited
    :return: template with ad edit form
    """
    ad = AdService.get_ad_by_id(ad_id)
    form = AdCreationForm()
    return render_template('ad_edit.html', ad=ad, form=form)


@login_required
def edit_ad(ad_id):
    """This function implements POST /ads/<ad_id>/edit end point.
    It edits given ad according to ad edit form.
    :param ad_id: id of the ad
    :return: redirect to /ad/<ad_id> end point
    """
    ad = AdService.get_ad_by_id(ad_id)
    ad_form = AdCreationForm(request.form)
    author_id = current_user.get_id()
    if ad_form.validate():
        AdService.edit_ad(ad, ad_form.data, author_id)
    else:
        show_error_messages(ad_form)
    return redirect(f'/ads/{ad_id}')
