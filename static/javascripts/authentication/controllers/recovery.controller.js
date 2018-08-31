/**
* Recovery controller
* @namespace cafeyoga.authentication.controllers
*/
(function () {
  'use strict';

  angular
    .module('cafeyoga.authentication.controllers')
    .controller('RecoveryController', RecoveryController);

  RecoveryController.$inject = ['$location','$http', '$scope', '$routeParams', 'Authentication', 'MessagingService'];

  /**
  * @namespace RegisterController
  */
  function RecoveryController($location, $http, $scope, $routeParams, Authentication, MessagingService) {
    var vm = this;

    activate();

    $scope.login = {};
    $scope.disableButton = true;
    $scope.account = undefined;
    $scope.token_invalid = undefined;
    $scope.loaded = false;

    /**
     * @name activate
     * @desc Actions to be performed when this controller is instantiated
     */
    function activate() {
        var path = $location.url().split('/');
        if( path[1] == "recovery" ){
           Authentication.getPasswordRecoveryInformation(path[2], function(success, data){
               console.log(data);
               $scope.email = data.email;
               if( success ){
                  $scope.token_invalid = false;
               }else{
                  $scope.token_invalid = "Le lien n'est pas valide ou a expiré. Veuillez effectuer une nouvelle demande de mot de passe";
               }
               $scope.loaded = true;
           })
        }
    }

    $scope.changeForm = function(){
       $scope.password_invalid = undefined;
    }

    $scope.changePassword = function(){
       if ($scope.login.password !== $scope.login.password2){
          $scope.password_invalid = "Mots de passes différents";
          return;
       }

       Authentication.updatePassword($scope.email,$scope.login.password,  function(success, data){
          if(success){
             Authentication.login($scope.email, $scope.login.password, false, function(success, data){
                $location.url('/');
             });
          }
       });
    }

    $scope.checkLoginEmail = function(){
        Authentication.checkAccountByEmail($scope.login.email, function(success, account){
           if(success){
              if( account.length == 1 ){
                 $scope.disableButton = false;
                 $scope.account = account[0];
              }else{
                 $scope.disableButton = true;
              }
           }else{
              $scope.disableButton = true;
           }
        });
    }

    $scope.newRecovery = function(){
        $location.url('/password-forgotten');
    }

    $scope.processRecovery = function(){
       Authentication.generatePasswordRecovery($scope.account, function(success, data){
          if(success){
             console.log(data);
             MessagingService.sendPasswordRecoveryEmail(data.email, data.token, function(success,data){})
             $location.url('/');
          }
       });
    }
  }
})();