from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Plan, Membresia


class PruebasPlanes(TestCase):

    def setUp(self):
        self.personal = User.objects.create_user(
            username='personal_prueba',
            password='ClavePrueba123!',
            is_staff=True
        )

        self.cliente = User.objects.create_user(
            username='cliente_prueba',
            password='ClavePrueba123!'
        )

        self.plan = Plan.objects.create(
            nombre='Plan mensual',
            descripcion='Acceso al gimnasio',
            precio=25000,
            duracion_dias=30,
            activo=True
        )

    def test_personal_puede_listar_planes(self):
        self.client.force_login(self.personal)

        respuesta = self.client.get(
            reverse('lista_planes')
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Plan mensual')

    def test_visitante_no_puede_listar_planes(self):
        respuesta = self.client.get(
            reverse('lista_planes')
        )

        self.assertEqual(respuesta.status_code, 302)

    def test_cliente_no_puede_listar_planes(self):
        self.client.force_login(self.cliente)

        respuesta = self.client.get(
            reverse('lista_planes')
        )

        self.assertEqual(respuesta.status_code, 403)
    def test_personal_puede_crear_plan(self):
        self.client.force_login(self.personal)

        respuesta = self.client.post(
            reverse('crear_plan'),
            {
                'nombre': 'Plan trimestral',
                'descripcion': 'Acceso por tres meses',
                'precio': '65000',
                'duracion_dias': 90,
                'activo': 'on'
            }
        )

        self.assertRedirects(
            respuesta,
            reverse('lista_planes')
        )

        self.assertTrue(
            Plan.objects.filter(
                nombre='Plan trimestral'
            ).exists()
        )

    def test_cliente_no_puede_crear_plan(self):
        self.client.force_login(self.cliente)

        respuesta = self.client.post(
            reverse('crear_plan'),
            {
                'nombre': 'Plan no autorizado',
                'precio': '10000',
                'duracion_dias': 30
            }
        )

        self.assertEqual(respuesta.status_code, 403)

        self.assertFalse(
            Plan.objects.filter(
                nombre='Plan no autorizado'
            ).exists()
        )
    def test_personal_puede_editar_plan(self):
        self.client.force_login(self.personal)

        respuesta = self.client.post(
            reverse('editar_plan', args=[self.plan.id]),
            {
                'nombre': 'Plan mensual actualizado',
                'descripcion': 'Acceso completo al gimnasio',
                'precio': '30000',
                'duracion_dias': 30,
                'activo': 'on'
            }
        )

        self.assertRedirects(
            respuesta,
            reverse('lista_planes')
        )

        self.plan.refresh_from_db()

        self.assertEqual(
            self.plan.nombre,
            'Plan mensual actualizado'
        )

        self.assertEqual(
            self.plan.precio,
            30000
        )

    def test_cliente_no_puede_editar_plan(self):
        self.client.force_login(self.cliente)

        respuesta = self.client.post(
            reverse('editar_plan', args=[self.plan.id]),
            {
                'nombre': 'Plan modificado sin permiso',
                'precio': '1000',
                'duracion_dias': 30
            }
        )

        self.assertEqual(respuesta.status_code, 403)

        self.plan.refresh_from_db()

        self.assertEqual(
            self.plan.nombre,
            'Plan mensual'
        )
    def test_personal_puede_eliminar_plan(self):
        self.client.force_login(self.personal)

        respuesta = self.client.post(
            reverse('eliminar_plan', args=[self.plan.id])
        )

        self.assertRedirects(
            respuesta,
            reverse('lista_planes')
        )

        self.assertFalse(
            Plan.objects.filter(id=self.plan.id).exists()
        )

    def test_cliente_no_puede_eliminar_plan(self):
        self.client.force_login(self.cliente)

        respuesta = self.client.post(
            reverse('eliminar_plan', args=[self.plan.id])
        )

        self.assertEqual(respuesta.status_code, 403)

        self.assertTrue(
            Plan.objects.filter(id=self.plan.id).exists()
        )
    def test_no_eliminar_plan_con_membresias(self):
        self.client.force_login(self.personal)

        Membresia.objects.create(
            cliente=self.cliente,
            plan=self.plan,
            fecha_inicio='2026-11-01',
            fecha_termino='2026-11-30',
            estado='ACTIVA'
        )

        respuesta = self.client.post(
            reverse('eliminar_plan', args=[self.plan.id])
        )

        self.assertRedirects(
            respuesta,
            reverse('lista_planes')
        )

        self.assertTrue(
            Plan.objects.filter(id=self.plan.id).exists()
        )

        self.assertTrue(
            Membresia.objects.filter(plan=self.plan).exists()
        )
