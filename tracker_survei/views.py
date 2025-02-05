from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import TrackerSurvei
from .serializers import TrackerSurveiSerializer, TrackerGet
from .serializers import TrackerSurveiSerializer, TrackerGet
import logging
from survei.models import Survei
from survei.serializers import SurveiGet, SurveiPost
from django.core.paginator import Paginator
from django.db.models import Q
from survei.models import Survei
from survei.serializers import SurveiGet, SurveiPost
from django.core.paginator import Paginator
from django.db.models import Q

logger = logging.getLogger(__name__)

class RolePermission:
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def has_permission(self, request, view):
        if not hasattr(request.user, 'role'):
            return False
        return request.user.role in self.allowed_roles

def validate_role_fields(user_role, data):
    """Validate that the user can only modify fields within their role."""
    role_field_mapping = {
        'Administrasi': {
            # Administrasi Awal fields
            'buat_kontrak', 'buat_invoice_dp', 
            'pembayaran_dp', 'pembuatan_kwitansi_dp',
            
            # Administrasi Akhir fields
            'buat_invoice_final', 'pembuatan_laporan', 
            'pembayaran_lunas', 'pembuatan_kwitansi_final', 
            'penyerahan_laporan'
        },
        'Pengendali Mutu': {
            'terima_info_survei', 'lakukan_survei', 
            'pantau_responden', 'pantau_data_cleaning'
        },
        'Logistik': {
            'terima_request_souvenir', 'ambil_souvenir'
        }
    }

    if user_role not in role_field_mapping:
        raise ValidationError(f"User role '{user_role}' does not have permission to modify any fields")

    allowed_fields = role_field_mapping.get(user_role, set())
    unauthorized_fields = set(data.keys()) - allowed_fields
    if unauthorized_fields:
        raise ValidationError(
            f"User with role '{user_role}' cannot modify these fields: {', '.join(unauthorized_fields)}"
        )

def safe_update_tracker(tracker, user_role, update_data):
    """Safely update tracker with validation and error handling."""
    try:
        validate_role_fields(user_role, update_data)
        
        # Save the current state of the tracker fields to allow rollback in case of error
        current_state = {
            field: getattr(tracker, field) 
            for field in update_data.keys()
        }
        
        # Attempt to update tracker with new data
        for field, value in update_data.items():
            setattr(tracker, field, value)
        
        # Perform model-level validation
        tracker.full_clean()
        tracker.save()
        
        return None  # Indicate no error
        
    except ValidationError as e:
        # Rollback to original state if validation fails
        for field, value in current_state.items():
            setattr(tracker, field, value)
        
        if hasattr(e, 'message_dict'):
            return e.message_dict  # Return validation error details
        return {'error': str(e)}
        
    except Exception as e:
        # Rollback to original state in case of any unexpected error
        for field, value in current_state.items():
            setattr(tracker, field, value)
            
        logger.error(f"Error updating tracker: {str(e)}")
        return {'error': 'An unexpected error occurred'}

def handle_tracker_update(request, survei_id, allowed_roles):
    """Helper function to handle tracker updates"""
    try:
        role_permission = RolePermission(allowed_roles)
        if not role_permission.has_permission(request, None):
            return Response(
                {"error": f"Access denied. Required roles: {', '.join(allowed_roles)}"},
                status=status.HTTP_403_FORBIDDEN
            )

        tracker = get_object_or_404(TrackerSurvei, survei_id=survei_id)
        error = safe_update_tracker(tracker, request.user.role, request.data)
        
        if error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = TrackerSurveiSerializer(tracker)
        return Response(serializer.data)
        
    except Exception as e:
        logger.error(f"Error updating tracker status: {str(e)}")
        return Response(
            {'error': 'An unexpected error occurred while updating the tracker'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @permission_classes([IsAuthenticated])
def get_tracker_detail(request, survei_id):
    try:
        survei = get_object_or_404(Survei, id=survei_id)
        tracker, created = TrackerSurvei.objects.get_or_create(survei=survei)
        serializer = TrackerSurveiSerializer(tracker)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching tracker detail: {str(e)}")
        return Response(
            {'error': 'Failed to fetch tracker details'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_administrasi_status(request, survei_id):
    """Update tracker status for Administrasi role."""
    return handle_tracker_update(request, survei_id, ['Administrasi'])

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_administrasi_akhir_status(request, survei_id):
    """Update tracker status for Administrasi Akhir role."""
    return handle_tracker_update(request, survei_id, ['Administrasi'])

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_logistik_status(request, survei_id):
    """Update tracker status for Logistik role."""
    return handle_tracker_update(request, survei_id, ['Logistik'])

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_pengendali_mutu_status(request, survei_id):
    """Update tracker status for Pengendali Mutu role."""
    return handle_tracker_update(request, survei_id, ['Pengendali Mutu'])

@api_view(['GET'])
def get_list_survei(request):
    # Get pagination parameters
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    search_query = request.GET.get('search', '')

    # Base queryset
    survei = Survei.objects.all()
    
    # Apply search if query exists
    if search_query:
        survei = survei.filter(
            Q(nama_survei__icontains=search_query) |
            Q(klien__nama_perusahaan__icontains=search_query) 
        )
    
    # Order by nama_survei
    survei = survei.order_by('nama_survei')
    
    # Create paginator
    paginator = Paginator(survei, page_size)

    try:
        page_obj = paginator.page(page_number)
    except:
        page_obj = paginator.page(1)

    # Serialize the paginated data
    serializer = SurveiPost(page_obj.object_list, many=True)
    
    # Prepare response data
    response_data = {
        'results': serializer.data,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'count': paginator.count,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
    }
    
    return Response(response_data)

@api_view(['GET'])
def get_list_dashboard(request):
    survei = TrackerSurvei.objects.all()
    serializer = TrackerGet(survei, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)