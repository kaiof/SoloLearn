if(Promise == undefined) {
// Straight copy from https://github.com/EvandroLG/P/blob/master/src/p.js, with the added check for already existing Promise
(function(){

  'use strict';

  var root = this;

  var Promise = function(context) {
    var callbacks = [];

    var execute = function(type, context, args) {
      var hasCallback = callbacks.length;

      if (!hasCallback) {
        return;
      }

      callbacks[0][type].apply(context, args);
      callbacks.shift();
    };

    return {
      context: context || root,

      resolve: function() {
        execute('fulfilled', this.context, arguments);
      },

      reject: function() {
        execute('rejected', this.context, arguments);
      },

      then: function(onFulfilled, onRejected) {
        callbacks.push({ 'fulfilled': onFulfilled, 'rejected': onRejected });
        return this;
      }
    };
  };

  root.P = {
    init: function(context) {
      return new Promise(context);
    }
  };

}).call(this);
}
