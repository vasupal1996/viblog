$(function () {

  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    start: function (e) {
    },

    stop: function (e) {
      location.reload()
    },

    // progressall: function (e, data) {
    //   var progress = parseInt(data.loaded / data.total * 100, 10);
    //   var strProgress = progress + "%";
    //   $(".progress-bar").css({"width": strProgress});
    //   $(".progress-bar").text(strProgress);
    // },

    done: function (data) {
    }

  });

});