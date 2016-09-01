$(function () {
  $('.montrose-filters').on('change', function () {
    var url = $(this).val();
    if (url) {
      window.location = url + '#search-data';
    }
    return false;
  });

 $(document).ready(function(){
      var disclaimerText = $('.hero-info .media-body');
      var disclaimerContainer = $('.media.hero-info');

      $('#newly-released-data-btn').on('click', function(){
        console.log('detected click');
        if($('#newly-released-data').hasClass('hidden')){
            $('#newly-released-data-btn').html('');
            $('#newly-released-data').removeClass('hidden');
            $('#newly-released-data-btn').html('<i class="fa fa-compress pull-right"></i>');

        }
        else{
            $('#newly-released-data-btn').html('');
            $('#newly-released-data').addClass('hidden');
            $('#newly-released-data-btn').html('<i class="fa fa-expand pull-right"></i>');
        }
      });

      // Click handler for the disclaimer icon.
      $('.hero-info > .media-left').click(function onMapDisclaimerClick(event) {
          var bodyWidth = $('body').outerWidth();
          var topPosition;

          if (disclaimerText.hasClass('hidden')) {
            topPosition = bodyWidth <= 976 ? '790px' : '295px';

            disclaimerText.removeClass('hidden');
            disclaimerContainer.css({
                'width': '300px',
                'padding': '10px',
                'top': topPosition
            });
          } else {
            topPosition = bodyWidth <= 976 ? '905px' : '410px';

            disclaimerText.addClass('hidden');
            disclaimerContainer.css({
                'width': '54px',
                'padding': '2px',
                'top': topPosition
            });
          }
      });

      // Reposition the disclaimer container on window resize.
      $(window).resize(function onWindowResize(event) {
          var bodyWidth = $('body').outerWidth();

          if (disclaimerText.hasClass('hidden')) {
            topPosition = bodyWidth <= 976 ? '905px' : '410px';
          } else {
            topPosition = bodyWidth <= 976 ? '790px' : '295px';
          }

          disclaimerContainer.css({'top': topPosition});
      });
  });

});

function toggleResources(resourceId) {
  $('#' + resourceId).toggleClass('hidden');
}