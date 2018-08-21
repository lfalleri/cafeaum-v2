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
       sendYogaConfirmationEmail: sendYogaConfirmationEmail,
       sendRestaurantReservationEmail: sendRestaurantReservationEmail,
       sendEmailFromContactPage:sendEmailFromContactPage,
    }

    return MessagingService;

    ////////////////////

    function sendYogaConfirmationEmail(lesson, account, nb_persons, callback) {
       return $http.post('api/v1/messaging/yoga_confirmation_email/', {
         lesson: lesson,
         account: account,
         nb_persons:nb_persons,
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
  }
})();

