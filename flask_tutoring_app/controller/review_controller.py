import werkzeug
from flask import request, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from service.review_service import ReviewService
from utils.forms import ReviewCreationForm, ResponseCreationForm, show_error_messages


@login_required
def ad_review(ad_id):
    """This function implements POST ad/<ad_id> end point.
    It adds review to the ad.
    :param: ad_id - id of the ad
    :returns: redirect to /ads/<ad_id> end point"""
    author = current_user.get_id()
    review_form = ReviewCreationForm(request.form)
    if review_form.validate():
        if ReviewService.add_review(review_form.data, author, ad_id):
            flash('Opinia dodana')
        else:
            flash('Dodałeś już opinię o tym ogłoszeniu')
    else:
        show_error_messages(review_form)
    return redirect(f'/ads/{ad_id}')


@login_required
def delete_review(review_id):
    """This function implements POST /reviews/<review_id>/delete end point.
    It deletes review.
    :param: review_id - id of the review
    :returns: redirect to /ads/<ad_id> end point"""
    user_id = current_user.get_id()
    flag, ad_id = ReviewService.delete_review(review_id, user_id)
    if flag:
        flash('Usunięto')
    else:
        flash('Nie udało się usunąć')
    return redirect(f'/ads/{ad_id}')


@login_required
def add_response(ad_id):
    """This function implements POST /ads/<ad_id>/add_response end point.
    It add response.
    :param: ad_id - id of the ad
    :returns: redirect to /ads/<ad_id> end point"""
    response_form = ResponseCreationForm(request.form)
    if response_form.validate():
        user_id = current_user.get_id()
        ReviewService.add_response(response_form.data, user_id)
    else:
        show_error_messages(response_form)
    return redirect(f'/ads/{ad_id}')


@login_required
def delete_response(response_id):
    """This function implements POST /responses/<response_id>/delete end point.
    It deletes response.
    :param: response_id - id of the response"""
    user_id = current_user.get_id()
    response = ReviewService.delete_response(response_id, user_id)
    if response:
        flash('Usunięto')
    else:
        flash('Nie udało się usunąć')
        raise werkzeug.exceptions.BadRequest
    return jsonify({'id': response_id})


def get_responses_by_review(review_id):
    """This function implements GET /reviews/<review_id>/responses end point.
    It gets page of responses of review with given id
    :param: review_id - id of the renview
    :returns: json object containing list of Responses"""
    page = request.args.get("page", type=int, default=1)
    responses = ReviewService.get_responses_by_review(review_id, page)
    return jsonify([response.as_dict() for response in responses])
