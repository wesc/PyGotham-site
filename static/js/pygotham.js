
/*
  Implements simple tabs. Expects markup like:

  <ul id="tabs">
    <li><a href="#content1">content 1</a></li>
    <li><a href="#content2">content 2</a></li>
  </ul>

  <div id="content1-content">some content 1</div>
  <div id="content2-content">some content 2</div>

  This starts it off:

  $("#tabs").pgtabs();

  pgtabs will then add "selected" classes onto the tab anchors, and
  the content divs. pgtabs appends "-content" to the href of the links
  to match the content div ids.
*/

$.fn.pgtabs = function() {
    var context = $(this);

    context.click(function() {
        context.removeClass("selected");
        $(this).addClass("selected");

        var tabs = context.map(function() {
            return $(this).attr("href") + "-content";
        });
        var sel = $(this).attr("href");
        tabs.each(function(index, tab) { $(tab).removeClass("selected"); });
        $(sel + "-content").addClass("selected");

        window.location.hash = sel;
        return false;
    });

    if (window.location.hash) {
        context.each(function() {
            if (window.location.hash == $(this).attr("href")) {
                $(this).click();
            }
        });
    }
}
