function sourcePlugin(opts) {
  'use strict';

  var player = this;

  var defaults = {
    'websocket_url': '/queue/',
  };

  var options = videojs.mergeOptions(defaults, opts);

  var source = $('<div id="source"></div>')[0];
  var source_icon = $('<div id="source_icon">i</div>')[0];
  var source_info = $('<div id="source_info">The title of the thing</div>')[0];
  $(source).append(source_icon);
  $(source).append(source_info);
  $(source_icon).click(function() { $(source_info).toggle(); });
  $(source_info).hide();

  var show_source = function(data) {
    var html = "";
    for (var key in data) {
      html += key + ": " + data[key] + '<br/>';
    }
    $(source_info).html(html);
    console.log(data);
  }

  var get_source = function() {
    $.getJSON('/queue/current', function(data) {
        show_source(data);
    });
  }

  player.el().appendChild(source);

  if (player.userActive() == true) { $(source).show(); }
  else { $(source).hide(); }

  player.on('useractive', function() { $(source).fadeIn() });
  player.on('userinactive', function() { $(source).fadeOut() });

  var queue = options.io.connect(options['websocket_url']);
  queue.on('change', get_source);
}
