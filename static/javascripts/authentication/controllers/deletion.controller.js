/**
* Deletion controller
* @namespace cafeyoga.authentication.controllers
*/
(function () {
  'use strict';

  angular
    .module('cafeyoga.authentication.controllers')
    .controller('DeletionController', DeletionController);

  DeletionController.$inject = ['$location','$http', '$scope', 'Authentication', 'MessagingService'];

  /**
  * @namespace RegisterController
  */
  function DeletionController($location, $http, $scope, Authentication, MessagingService) {
    var vm = this;

    activate();

    $scope.deletePassword = {};
    $scope.deletePassword;
    $scope.account = undefined;
    $scope.loaded = false;

    /**
     * @name activate
     * @desc Actions to be performed when this controller is instantiated
     */
    function activate() {

       Authentication.getFullAccount(function(value){
           $scope.account = value;
           if(angular.equals($scope.account,{})){
              /* Non loggé -> /monespace */
              $location.url('/monespace');
           }
       });
    }

    $scope.changeForm = function(){
       $scope.error = undefined;
    }

    $scope.cancelDeletion = function(){
        $location.url('/');
    }

    $scope.processDeletion = function(){
        Authentication.checkPassword(
            $scope.account.id,
            $scope.password,
            function(success, message){
                if(!success){
                    $scope.error = message;
                }else{
                    Authentication.logout(false);

                    Authentication.deleteProfile(
                        $scope.account.id,
                        $scope.password,
                        function(success, message){
                            if(!success){
                                $scope.error = message;
                            }else{
                               MessagingService.sendAccountDeletionToStaffEmail(
                                   $scope.account.first_name,
                                   $scope.account.last_name,
                                   $scope.account.email,
                                   $scope.account.id,
                                   function(success, message){}
                               );
                               MessagingService.sendAccountDeletionToCustomerEmail(
                                   $scope.account.first_name,
                                   $scope.account.last_name,
                                   $scope.account.email,
                                   function(success, message){}
                               );

                               $scope.success = "Votre compte a bien été supprimé";
                            }
                        }
                    );
                }
            }
        );
    }
  }
})();