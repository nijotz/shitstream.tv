(function(window, videojs, io) {
  'use strict';

  var defaults = {
    'websocket_url': '/queue/',
  };

  var source = $('<div id="source"></div>')[0];
  var source_icon = $('<div id="source_icon">i</div>')[0];
  var source_info = $('<div id="source_info">The title of the thing</div>')[0];
  $(source).append(source_icon);
  $(source).append(source_info);
  $(source_icon).click(function() { $(source_info).toggle(); });
  $(source_info).hide();

  var update_source = function(data) {
    $(source_info).html(data)
    console.log(data);
  }

  var init = function(options) {
    var settings = videojs.util.mergeOptions(defaults, options);
    var player = this;

    player.el().appendChild(source);

    if (player.userActive() == true) { $(source).show(); }
    else { $(source).hide(); }

    player.on('useractive', function() { $(source).fadeIn() });
    player.on('userinactive', function() { $(source).fadeOut() });

    var queue = io.connect(settings['websocket_url']);
    queue.on('change', function(data) { update_source(data); });
  };

  videojs.plugin('source', init);
})(window, window.videojs, window.io);
