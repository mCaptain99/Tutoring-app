toggle = () => {
   let btn = $("#btn_toggle");
   let ads_div = $('#my_ads');
   let reviews_div = $('#my_reviews');
   if (ads_div.css("display") == "block"){
        ads_div.css("display", "none");
        reviews_div.css("display", "block");
        btn.text("Moje ogłoszniea");
   }
   else{
        reviews_div.css("display", "none");
        ads_div.css("display", "block");
        btn.text("Moje opinie");
   }
}