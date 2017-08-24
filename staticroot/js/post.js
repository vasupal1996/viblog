$(function () {

  




  $("#publish").click(function (e) {
    e.preventDefault();
    $("input[name='status']").val("P");
    $('#create-or-edit').attr('action', '/publish/')
    $("#create-or-edit").submit();
  });

  $("#draft").click(function (e) {
    e.preventDefault();
    $("input[name='status']").val("D");
    $('#create-or-edit').attr('action', '/draft/')
    $("#create-or-edit").submit();
  });
});