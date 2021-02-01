#!/bin/bash

function listprogs(){
  pacman -Qlq "$@" | grep -Po "(?<=${PATH//://|}).*"
}

listprogs "$@"
