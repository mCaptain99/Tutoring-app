render_evaluation = (p_id, evaluation) => {
    number = evaluation.split('.');
    if (number[0] == 0){
        $(`#${p_id}`).append(
            '<i style="color:#114084;" class="far fa-star"></i>'
        )
    }
    for (let i=1; i<=parseInt(number[0]); i++){
        $(`#${p_id}`).append(
            '<i style="color:#114084;" class="fas fa-star"></i>'
        )
    }
    if (parseInt(number[1][0]) >= 2){
        $(`#${p_id}`).append(
            '<i style="color:#114084;;" class="fas fa-star-half"></i>'
        )};
}