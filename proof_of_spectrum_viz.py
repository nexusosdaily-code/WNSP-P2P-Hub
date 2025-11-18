"""
Proof of Spectrum Visualization Module
=======================================

Interactive visualizations for wavelength-based consensus
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import List, Dict
from proof_of_spectrum import (
    ProofOfSpectrumConsensus, SpectralValidator, SpectralRegion,
    SpectralBlock, InterferencePattern
)


def get_spectral_color(region: SpectralRegion) -> str:
    """Get RGB color for spectral region"""
    colors = {
        SpectralRegion.VIOLET: '#8B00FF',
        SpectralRegion.BLUE: '#0000FF',
        SpectralRegion.GREEN: '#00FF00',
        SpectralRegion.YELLOW: '#FFFF00',
        SpectralRegion.ORANGE: '#FF8C00',
        SpectralRegion.RED: '#FF0000'
    }
    return colors[region]


def visualize_spectral_distribution(consensus: ProofOfSpectrumConsensus) -> go.Figure:
    """
    Visualize validator distribution across electromagnetic spectrum
    """
    distribution = consensus.get_spectral_distribution()
    
    regions = []
    validator_counts = []
    total_stakes = []
    colors = []
    wavelength_ranges = []
    
    for region in SpectralRegion:
        validators = distribution[region]
        regions.append(region.region_name.capitalize())
        validator_counts.append(len(validators))
        total_stakes.append(sum(v.stake for v in validators))
        colors.append(get_spectral_color(region))
        wavelength_ranges.append(f"{region.wavelength_min}-{region.wavelength_max}nm")
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Validator Count by Spectral Region', 'Stake Distribution by Region'),
        specs=[[{'type': 'bar'}, {'type': 'bar'}]]
    )
    
    # Validator count
    fig.add_trace(
        go.Bar(
            x=regions,
            y=validator_counts,
            marker_color=colors,
            name='Validators',
            text=validator_counts,
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Validators: %{y}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Stake distribution
    fig.add_trace(
        go.Bar(
            x=regions,
            y=total_stakes,
            marker_color=colors,
            name='Total Stake',
            text=[f'{s:,.0f}' for s in total_stakes],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Total Stake: %{y:,.0f}<extra></extra>'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        title_text="Spectral Network Distribution",
        title_x=0.5
    )
    
    fig.update_xaxes(title_text="Spectral Region", row=1, col=1)
    fig.update_xaxes(title_text="Spectral Region", row=1, col=2)
    fig.update_yaxes(title_text="Validator Count", row=1, col=1)
    fig.update_yaxes(title_text="Total Stake", row=1, col=2)
    
    return fig


def visualize_spectrum_coverage(consensus: ProofOfSpectrumConsensus) -> go.Figure:
    """
    Visualize electromagnetic spectrum coverage
    """
    distribution = consensus.get_spectral_distribution()
    
    fig = go.Figure()
    
    # Draw spectrum bar
    for region in SpectralRegion:
        validators = distribution[region]
        coverage_pct = (len(validators) / max(1, len(consensus.validators))) * 100
        
        fig.add_trace(go.Bar(
            x=[region.bandwidth],
            y=['Spectrum'],
            orientation='h',
            name=region.region_name.capitalize(),
            marker=dict(
                color=get_spectral_color(region),
                line=dict(color='white', width=2)
            ),
            text=f"{region.region_name}<br>{len(validators)} validators<br>{region.wavelength_min}-{region.wavelength_max}nm",
            textposition='inside',
            hovertemplate=f'<b>{region.region_name.capitalize()}</b><br>' +
                         f'Range: {region.wavelength_min}-{region.wavelength_max}nm<br>' +
                         f'Validators: {len(validators)}<br>' +
                         f'Coverage: {coverage_pct:.1f}%<extra></extra>'
        ))
    
    fig.update_layout(
        title='Electromagnetic Spectrum Coverage (380-750nm)',
        barmode='stack',
        height=200,
        showlegend=False,
        xaxis_title='Wavelength (nm)',
        yaxis_showticklabels=False
    )
    
    return fig


def visualize_interference_pattern(pattern: InterferencePattern) -> go.Figure:
    """
    Visualize wave interference pattern from multiple validators
    """
    if not pattern.signatures:
        return go.Figure()
    
    # Create wavelength data
    wavelengths = []
    amplitudes = []
    colors = []
    region_names = []
    
    for region, signature in pattern.signatures.items():
        # Convert signature to "amplitude" (hash-based)
        amplitude = int(signature[:8], 16) / (16**8)  # Normalize 0-1
        
        wavelengths.append(region.center_wavelength)
        amplitudes.append(amplitude)
        colors.append(get_spectral_color(region))
        region_names.append(region.region_name.capitalize())
    
    fig = go.Figure()
    
    # Plot signatures as spectral lines
    fig.add_trace(go.Scatter(
        x=wavelengths,
        y=amplitudes,
        mode='markers+lines',
        marker=dict(
            size=15,
            color=colors,
            line=dict(color='white', width=2)
        ),
        line=dict(color='gray', width=2, dash='dash'),
        text=region_names,
        hovertemplate='<b>%{text}</b><br>Wavelength: %{x}nm<br>Amplitude: %{y:.3f}<extra></extra>'
    ))
    
    # Add spectral coverage bands
    for region in pattern.signatures.keys():
        fig.add_vrect(
            x0=region.wavelength_min,
            x1=region.wavelength_max,
            fillcolor=get_spectral_color(region),
            opacity=0.1,
            line_width=0
        )
    
    fig.update_layout(
        title='Wave Interference Pattern (Multi-Spectral Signatures)',
        xaxis_title='Wavelength (nm)',
        yaxis_title='Normalized Amplitude',
        height=400,
        showlegend=False,
        xaxis=dict(range=[370, 760])
    )
    
    return fig


def visualize_attack_resistance(attack_results: List[Dict]) -> go.Figure:
    """
    Visualize 51% attack resistance across different control percentages
    """
    df = pd.DataFrame(attack_results)
    
    fig = go.Figure()
    
    # Attack success/failure
    fig.add_trace(go.Scatter(
        x=df['attacker_control_pct'],
        y=df['attacker_spectral_regions'],
        mode='lines+markers',
        name='Attacker Spectral Coverage',
        line=dict(color='red', width=3),
        marker=dict(size=10)
    ))
    
    # Required threshold
    required = df['required_spectral_regions'].iloc[0]
    fig.add_hline(
        y=required,
        line_dash='dash',
        line_color='green',
        annotation_text=f'Required: {required} regions',
        annotation_position='right'
    )
    
    # Color background based on attack possibility
    for i, row in df.iterrows():
        color = 'rgba(255,0,0,0.1)' if row['attack_possible'] else 'rgba(0,255,0,0.1)'
        if i < len(df) - 1:
            fig.add_vrect(
                x0=row['attacker_control_pct'],
                x1=df.iloc[i+1]['attacker_control_pct'],
                fillcolor=color,
                line_width=0
            )
    
    fig.update_layout(
        title='51% Attack Resistance Analysis',
        xaxis_title='Attacker Control (%)',
        yaxis_title='Spectral Regions Controlled',
        height=400,
        showlegend=True
    )
    
    return fig


def create_attack_resistance_table(attack_results: List[Dict]) -> pd.DataFrame:
    """Create detailed table of attack resistance results"""
    df = pd.DataFrame(attack_results)
    
    # Format for display
    display_df = pd.DataFrame({
        'Control %': df['attacker_control_pct'].apply(lambda x: f"{x:.0f}%"),
        'Validators': df['attacker_validator_count'],
        'Spectral Regions': df['attacker_spectral_regions'],
        'Required': df['required_spectral_regions'],
        'Attack Possible': df['attack_possible'].apply(lambda x: '❌ YES' if x else '✅ NO'),
        'Status': df['security_status'].apply(lambda x: '🔴 VULNERABLE' if x == 'VULNERABLE' else '🟢 SECURE')
    })
    
    return display_df


def visualize_validator_wavelengths(validators: List[SpectralValidator]) -> go.Figure:
    """
    Show individual validator wavelengths across the spectrum
    """
    wavelengths = [v.wavelength for v in validators]
    regions = [v.spectral_region.region_name.capitalize() for v in validators]
    colors_list = [get_spectral_color(v.spectral_region) for v in validators]
    stakes = [v.stake for v in validators]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=wavelengths,
        y=[1] * len(wavelengths),
        mode='markers',
        marker=dict(
            size=[np.log10(s + 1) * 5 for s in stakes],  # Size by stake
            color=colors_list,
            line=dict(color='white', width=1),
            opacity=0.7
        ),
        text=[f"{v.validator_id}<br>λ={v.wavelength:.1f}nm<br>Stake={v.stake:.0f}" 
              for v in validators],
        hovertemplate='%{text}<extra></extra>'
    ))
    
    # Add region boundaries
    for region in SpectralRegion:
        fig.add_vline(
            x=region.wavelength_min,
            line_dash='dot',
            line_color='gray',
            opacity=0.5
        )
    
    fig.update_layout(
        title='Validator Wavelength Distribution',
        xaxis_title='Wavelength (nm)',
        yaxis_visible=False,
        height=200,
        showlegend=False,
        xaxis=dict(range=[370, 760])
    )
    
    return fig
