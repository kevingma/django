from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models.functions import ExtractYear
from django.db.models import Count
import plotly.graph_objs as go
from plotly.offline import plot

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = Voter.objects.all()
        queryset = queryset.annotate(birth_year=ExtractYear('date_of_birth'))

        party = self.request.GET.get('party_affiliation')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')
        voter_score = self.request.GET.get('voter_score')
        elections = self.request.GET.getlist('elections')

        if party:
            queryset = queryset.filter(party_affiliation=party)
        if min_year:
            queryset = queryset.filter(birth_year__gte=int(min_year))
        if max_year:
            queryset = queryset.filter(birth_year__lte=int(max_year))
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))
        if elections:
            for election in elections:
                filter_kwargs = {election: True}
                queryset = queryset.filter(**filter_kwargs)

        return queryset.order_by('last_name', 'first_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request

        context['party_list'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        years = Voter.objects.annotate(
            birth_year=ExtractYear('date_of_birth')
        ).values_list('birth_year', flat=True).distinct()
        context['years_list'] = sorted(years)

        context['voter_scores'] = Voter.objects.values_list('voter_score', flat=True).distinct().order_by('voter_score')
        context['election_fields'] = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        context['election_labels'] = {
            'v20state': '2020 State Election',
            'v21town': '2021 Town Election',
            'v21primary': '2021 Primary Election',
            'v22general': '2022 General Election',
            'v23town': '2023 Town Election',
        }

        context['selected_elections'] = self.request.GET.getlist('elections')

        return context

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class VoterGraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        queryset = Voter.objects.all()
        queryset = queryset.annotate(birth_year=ExtractYear('date_of_birth'))

        party = self.request.GET.get('party_affiliation')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')
        voter_score = self.request.GET.get('voter_score')
        elections = self.request.GET.getlist('elections')

        if party:
            queryset = queryset.filter(party_affiliation=party)
        if min_year:
            queryset = queryset.filter(birth_year__gte=int(min_year))
        if max_year:
            queryset = queryset.filter(birth_year__lte=int(max_year))
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))
        if elections:
            for election in elections:
                filter_kwargs = {election: True}
                queryset = queryset.filter(**filter_kwargs)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()


        birth_years = queryset.values('birth_year').annotate(count=Count('id')).order_by('birth_year')
        years = [entry['birth_year'] for entry in birth_years]
        counts = [entry['count'] for entry in birth_years]

        fig_birth_year = go.Figure(data=[go.Bar(x=years, y=counts)])
        fig_birth_year.update_layout(
            title='Voter Distribution by Year of Birth',
        )
        graph_birth_year = plot(fig_birth_year, output_type='div', include_plotlyjs=False)

        party_counts = queryset.values('party_affiliation').annotate(count=Count('id'))
        parties = [entry['party_affiliation'] for entry in party_counts]
        party_counts_list = [entry['count'] for entry in party_counts]

        fig_party = go.Figure(data=[go.Pie(labels=parties, values=party_counts_list)])
        fig_party.update_layout(title='Distribution of Voters by Party Affiliation')
        graph_party = plot(fig_party, output_type='div', include_plotlyjs=False)

        election_fields = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']

        election_data = []
        for field in election_fields:
            count = queryset.filter(**{field: True}).count()
            election_data.append({'election': field, 'count': count})

        election_names = [d['election'] for d in election_data]
        election_counts = [d['count'] for d in election_data]

        fig_elections = go.Figure(data=[go.Bar(x=election_names, y=election_counts)])
        fig_elections.update_layout(
            title='Vote Count by Election',
        )
        fig_elections.update_yaxes(
            tickformat=',',
            dtick=1000
        )
        graph_elections = plot(fig_elections, output_type='div', include_plotlyjs=False)

        context['graph_birth_year'] = graph_birth_year
        context['graph_party'] = graph_party
        context['graph_elections'] = graph_elections

        context['request'] = self.request

        context['party_list'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        all_years = Voter.objects.annotate(
            birth_year=ExtractYear('date_of_birth')
        ).values_list('birth_year', flat=True).distinct()
        context['years_list'] = sorted(all_years)

        context['voter_scores'] = Voter.objects.values_list('voter_score', flat=True).distinct().order_by('voter_score')

        elections = []
        for field in election_fields:
            elections.append({'field': field, 'label': field})

        context['elections'] = elections
        context['selected_elections'] = self.request.GET.getlist('elections')

        return context