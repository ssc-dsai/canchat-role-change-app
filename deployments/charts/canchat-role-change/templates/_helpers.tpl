{{/*
Expand the name of the chart.
*/}}
{{- define "canchat-role-change.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "canchat-role-change.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "canchat-role-change.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "canchat-role-change.labels" -}}
helm.sh/chart: {{ include "canchat-role-change.chart" . }}
{{ include "canchat-role-change.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "canchat-role-change.selectorLabels" -}}
app.kubernetes.io/name: {{ include "canchat-role-change.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Define Allowed Postgresql SSL Mode
*/}}
{{- define "allowedSSLModes" -}}
  disable, require, verify-ca, verify-full
{{- end -}}

{{- define "validate.sslmode" -}}
{{- $sslmode := .Values.postgresql.sslmode -}}
{{- $allowed := splitList ", " (include "allowedSSLModes" .) -}}

{{- if not (has $sslmode $allowed) -}}
{{- fail (printf "Invalid sslmode '%s'. Allowed values are: %v" $sslmode $allowed) -}}
{{- end -}}
{{- end -}}