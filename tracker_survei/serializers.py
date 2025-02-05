from rest_framework import serializers
from .models import TrackerSurvei
from survei.serializers import SurveiGet

class TrackerSurveiSerializer(serializers.ModelSerializer):
    nama_survei = serializers.CharField(source='survei.nama_survei', read_only=True)
    nama_klien = serializers.CharField(source='survei.nama_klien', read_only=True)
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = TrackerSurvei
        fields = ['id', 'nama_survei', 'nama_klien', 'status', 'last_status']
    
    def get_status(self, obj):
        status_fields = [
            # Administrasi Awal
            'buat_kontrak', 'buat_invoice_dp', 'pembayaran_dp', 'pembuatan_kwitansi_dp',
            # Logistik
            'terima_request_souvenir', 'ambil_souvenir',
            # Pengendali Mutu
            'terima_info_survei', 'lakukan_survei', 'pantau_responden', 'pantau_data_cleaning',
            # Administrasi Akhir
            'buat_invoice_final', 'pembuatan_laporan', 'pembayaran_lunas', 
            'pembuatan_kwitansi_final', 'penyerahan_laporan'
        ]
        return [{field: getattr(obj, field)} for field in status_fields]

class TrackerGet(serializers.ModelSerializer):
    survei = SurveiGet()
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = TrackerSurvei
        fields = ("id", "survei", "status", "last_status")
    
    def get_status(self, obj):
        status_fields = [
            # Administrasi Awal
            'buat_kontrak', 'buat_invoice_dp', 'pembayaran_dp', 'pembuatan_kwitansi_dp',
            # Logistik
            'terima_request_souvenir', 'ambil_souvenir',
            # Pengendali Mutu
            'terima_info_survei', 'lakukan_survei', 'pantau_responden', 'pantau_data_cleaning',
            # Administrasi Akhir
            'buat_invoice_final', 'pembuatan_laporan', 'pembayaran_lunas', 
            'pembuatan_kwitansi_final', 'penyerahan_laporan'
        ]
        return [{field: getattr(obj, field)} for field in status_fields]