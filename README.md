# Análisis y control de los productos de aceite de palma

## Introducción

La solución propuesto implementará un sistema para facilitar la evaluación de proveedores de commodities, específicamente centrado en el **aceite de palma**. Este sistema combina información de múltiples fuentes através de APIs y hojas de cálculo con datos de proveedores. Los datos son almacenados en un *Data Warehouse*, mientras que los precios del aceite de palma son consultados en tiempo real dada su volatilidad. Los datos se visualizan a través de un panel intuitivo, ofreciendo a los usuarios acceso dinámico y consolidado a indicadores críticos para la toma de decisiones estratégicas, asegurando sostenibilidad, transparencia y competitividad en la cadena de suministro.

## Arquitectura

En la Capa de Lógica, los datos son gestionados mediante un proceso ETL (Extract, Transform, Load) para almacenamiento en un Data Warehouse, mientras que un esquema mediado permite consultas en tiempo real sin almacenamiento persistente. En la Capa de Presentación, los datos se visualizan a través de un panel intuitivo:

![image](./documentation/arquitectura-implementada.png)


## Primeros pasos

```
# Technical prerequisites

# Ubuntu or Debian
sudo apt update
sudo apt install podman

# Fedora
sudo dnf install podman

# MacOS
brew install podman

# Install Podman Compose
sudo pip3 install podman-compose

# Test installation
podman-compose --version

# End Technical prerequisites

# Run the application
podman-compose up --build

# Test application running
podman ps

# Shutdown the application
podman-compose down

```

## APIs disponibles

```
http://localhost:5001/ # Test disponibilidad
http://localhost:5001/api/stock_price?stock_symbols=AMZN,CMCSA # Ejemplo para obtener los precios de Amazon y Comcast
http://localhost:5001/api/data # Lista de proveedores de aceite agrupados por paises

```

## Resolver Problemas

Si falla all levantar el sistema puede que sea debido a la falta de un entorno para desplegar los contenedores del sistema

```
# Comprueba que hay una maquina virtual disponible
podman machine ls 

# En caso de haber ninguna
podman machine start
```

Hay conflictos que nombre de imagenes existentes o solapamientos con puertos.

```
# Cuidado, el siguiente comando borrara todos los contenedores y otros recursos que hayas creado hasta el momento
podman system prune -a

```

## Equipo

* Nuria González Hernández
* Raquel Cristina Castro Núñez
* Jorge Ramos Santana
* Jorge Blanco Gómez
* Carlos Ignacio Salinas Gancedo

