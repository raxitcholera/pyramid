# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>

<h1> User Login </h1>

<form action="${request.route_url('login')}" method="post">
  <input type="text" maxlength="100" name="UserName">
  <input type="password" maxlength="100" name="Password">
  <input type="submit" name="login" value="LOGIN" class="button">
</form>