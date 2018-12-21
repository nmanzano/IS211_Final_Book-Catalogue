function search_title_query() {
    var search_ISBN = document.getElementById('search_field').value;
    document.getElementById('search_field').value = "";

    $.ajax({
      url: 'https://www.googleapis.com/books/v1/volumes?q=' + search_ISBN,
      dataType: 'json',

      success: function(data) {
        $( "#book_results" ).show();
        var counter = 0;
        for (var i = 0; i < data.items.length; i++) {
          counter++;
          if (counter <= 1) {
            if (data.items[0].volumeInfo.title){
              $("#title").val(data.items[0].volumeInfo.title);
            }
            else {
              $("#title").val('Data Unavailable');
            }
            if (data.items[0].volumeInfo.authors) {
              $("#author").val(data.items[0].volumeInfo.authors);
            }
            else {
              $("#author").val('Data Unavailable');
            }
            if (data.items[0].volumeInfo.pageCount) {
              $("#page_count").val(data.items[0].volumeInfo.pageCount);
            }
            else {
              $("#page_count").val('Data Unavailable');
            }
            if (data.items[0].volumeInfo.averageRating) {
              $("#rating").val(data.items[0].volumeInfo.averageRating);
            }
            else {
              $("#rating").val('Data Unavailable');
            }
            $("#thumbnail").remove();
            $('#book_cover').append('<div id="thumbnail"><img src="'+data.items[0].volumeInfo.imageLinks.smallThumbnail+'"></div>');
          }
        }
      },

      type: 'Get'
    });
}

$( document ).ready(function() {
  if ( $('#book_results').css('display') || $('#book_results').css("visibility") == "show"){
    document.getElementById('title').value = "";
    document.getElementById('author').value = "";
    document.getElementById('page_count').value = "";
    document.getElementById('rating').value = "";
  }
  $("#book_results").hide();
  var element = document.getElementById('return_results');
  element.addEventListener('click', search_title_query, false);
});
