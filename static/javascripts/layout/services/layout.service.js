/**
* Layout
* @namespace thinkster.authentication.services
*/
(function () {
  'use strict';

  angular
    .module('cafeyoga.layout.services')
    .factory('Layout', Layout);

  Layout.$inject = ['$cookies','$mdMedia'];

  /**
  * @namespace Authentication
  * @returns {Factory}
  */
  function Layout($cookies, $mdMedia) {

    var Layout = {
      detectScreenOrientation: detectScreenOrientation,
      detectMdScreen: detectMdScreen,
      detectGtMdScreen: detectGtMdScreen,
      setUserAcceptedCookies:setUserAcceptedCookies,
      getUserAcceptedCookies:getUserAcceptedCookies,
      cookiesAcceptedForSession:false,

      toastShown: false,
      isToastShown:isToastShown,
      toastShow : toastShow,
      toastHide : toastHide,

      setSideNavBarToRecharge: setSideNavBarToRecharge,
      unsetSideNavBarToRecharge:unsetSideNavBarToRecharge,
      getSideNavBarToRecharge: getSideNavBarToRecharge,
      sideNavBarToRecharge : false,
    };

    return Layout;

    function detectScreenOrientation() {
       return $mdMedia('portrait');
    }

    function detectMdScreen(){
       return $mdMedia('md');
    }

    function detectGtMdScreen(){
       return $mdMedia('gt-md');
    }

    function setUserAcceptedCookies(){
       $cookies.userAcceptedCookies = 'true';
       window.localStorage.setItem('userAcceptedCookies','true');
       Layout.cookiesAcceptedForSession = true;
    }

    function getUserAcceptedCookies(){
       var storage = window.localStorage.getItem('userAcceptedCookies');
       if (Layout.cookiesAcceptedForSession || storage || $cookies.userAcceptedCookies) {
          return true;
       }
       return false;
    }

    function isToastShown(){
       return Layout.toastShown;
    }

    function toastShow(){
      Layout.toastShown = true;
    }

    function toastHide(){
      Layout.toastShown = false;
    }

    function setSideNavBarToRecharge(){
       if( Layout.sideNavBarToRecharge==false ){
          Layout.sideNavBarToRecharge=true;
       }
    }

    function unsetSideNavBarToRecharge(){
       if( Layout.sideNavBarToRecharge==true ){
          Layout.sideNavBarToRecharge=false;
       }
    }

    function getSideNavBarToRecharge(){
        return Layout.sideNavBarToRecharge;
    }
  }
})();