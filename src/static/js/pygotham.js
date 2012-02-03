
/*
  Implements simple tabs. Expects markup like:

  <ul id="tabs">
    <li><a href="#content1">content 1</a></li>
    <li><a href="#content2">content 2</a></li>
  </ul>

  <div id="content1">some content 1</div>
  <div id="content2">some content 2</div>

  This starts it off:

  $("#tabs").pgtabs();

  pgtabs will then add "selected" classes onto the tab anchors, and
  the content divs. The href match content ids.
*/
$.fn.pgtabs = function() {
    var context = $(this);

    context.click(function() {
        context.removeClass("selected");
        $(this).addClass("selected");

        var tabs = context.map(function() {
            return $(this).attr("href");
        });
        var sel = $(this).attr("href");
        tabs.each(function(index, tab) { $(tab).removeClass("selected"); });
        $(sel).addClass("selected");

        return false;
    });
}
