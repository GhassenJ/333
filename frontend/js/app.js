'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', [
  'ngRoute',
  'myApp.filters',
  'myApp.services',
  'myApp.directives',
  'myApp.controllers'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/many', {templateUrl: 'partials/many.html', controller: 'Many'});
  $routeProvider.when('/single', {templateUrl: 'partials/single.html', controller: 'Single'});
  $routeProvider.otherwise({redirectTo: '/many'});
}]);
