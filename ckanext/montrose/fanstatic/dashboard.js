$(function () {
  $('.montrose-filters').on('change', function () {
    var url = $(this).val();
    if (url) {
      window.location = url + '#search-data';
    }
    return false;
  });
});

function toggleResources(resourceId) {
  $('#' + resourceId).toggleClass('hidden');
}