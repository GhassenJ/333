'use strict';

/* Controllers */

angular.module('myApp.controllers', [])
  .controller('Many', ['$scope', '$http', function($scope, $http) {
      
      //$scope.base = 'http://princeton-marketplace.appspot.com/';
      $scope.base = '';
      $scope.dict = {
        "home" : null,
        "but_posts" : null,
        "sell_posts" : null,
        "my_open_posts" : null,
        "my closed_posts" : null,
        "my_responded_posts" : null
      };
      $scope.getPosts = function(url) {
        $http.get($scope.base + url).success(function (data) { $scope.dict[url] = data; });
        $scope.last = url;
      }
      
  }])
  .controller('Single', [function() {

  }]);
