/**
* Authentication
* @namespace thinkster.authentication.services
*/
(function () {
  'use strict';

  angular
    .module('cafeyoga.utils.services')
    .factory('MessagingService', MessagingService);

  MessagingService.$inject = ['$http','$q'];

  /**
  * @namespace Reservations
  * @returns {Factory}
  */
  function MessagingService($http, $q) {
    /**
    * @name Reservations
    * @desc The Factory to be returned
    */
    var MessagingService = {
       sendAccountCreationEmail:sendAccountCreationEmail,
       sendYogaConfirmationEmail: sendYogaConfirmationEmail,
       sendYogaCancellationEmail: sendYogaCancellationEmail,
       sendRestaurantReservationEmail: sendRestaurantReservationEmail,
       sendEmailFromContactPage:sendEmailFromContactPage,
       sendPasswordRecoveryEmail:sendPasswordRecoveryEmail,
    }

    return MessagingService;

    ////////////////////
    function sendAccountCreationEmail(email,  callback) {
       return $http.post('api/v1/messaging/account_creation_email/', {
         email: email,
       }).then(
         function(data, status, headers, config){
           callback(true, "OK");
       },function(data, status, headers, config){
           callback(false, ["Une erreur est survenue lors de la réservation"]);
       });
    }

    function sendYogaConfirmationEmail(lesson, account, nb_persons, reservation_id, callback) {
       return $http.post('api/v1/messaging/yoga_confirmation_email/', {
         lesson: lesson,
         account: account,
         nb_persons:nb_persons,
         reservation_id: reservation_id,
       }).then(
         function(data, status, headers, config){
           callback(true, "OK");
       },function(data, status, headers, config){
           callback(false, ["Une erreur est survenue lors de la réservation"]);
       });
    }

    function sendYogaCancellationEmail(lesson, account, callback) {
       return $http.post('api/v1/messaging/yoga_cancellation_email/', {
         lesson: lesson,
         account: account,
       }).then(
         function(data, status, headers, config){
           callback(true, "OK");
       },function(data, status, headers, config){
           callback(false, ["Une erreur est survenue lors de la réservation"]);
       });
    }

    function sendRestaurantReservationEmail(reservation_information,personal_information, callback) {
       return $http.post('api/v1/messaging/restaurant_reservation_email/', {
         reservation_information: reservation_information,
         personal_information: personal_information,
       }).then(
         function(data, status, headers, config){
           callback(true, "OK");
       },function(data, status, headers, config){
           callback(false, ["Une erreur est survenue lors de la réservation"]);
       });
    }

    function sendEmailFromContactPage(type, name, email, tel, message, callback) {
       return $http.post('api/v1/messaging/contact/', {
         type: type,
         name: name,
         email: email,
         tel: tel,
         message: message,
       }).then(
         function(data, status, headers, config){
           callback(true, "OK");
       },function(data, status, headers, config){
           callback(false, ["Une erreur est survenue lors de la réservation"]);
       });
    }

    function sendPasswordRecoveryEmail(email, token, callback) {
       return $http.post('api/v1/messaging/recovery/', {
         email: email,
         token: token,
       }).then(
         function(data, status, headers, config){
           callback(true, "OK");
       },function(data, status, headers, config){
           callback(false, ["Une erreur est survenue lors de la réservation"]);
       });
    }

  }
})();

