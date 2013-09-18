# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>

<h1>Add a new User</h1>
  
    <span>
              <a href="${request.application_url}/logout">Logout</a>
    </span>

<form action="${request.route_url('new')}" method="post">
  <input type="text" maxlength="100" name="UserName">
  <input type="password" maxlength="100" name="Password">
  <input type="submit" name="add" value="ADD" class="button">
</form>